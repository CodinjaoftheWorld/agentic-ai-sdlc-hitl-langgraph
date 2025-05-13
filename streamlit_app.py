# app.py
import os
import streamlit as st
from dotenv import load_dotenv
from langgraph.checkpoint.memory import MemorySaver
from sdlc_graph import (
    graph,  # your compiled LangGraph
    State,  # your TypedDict state schema
)

load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

st.set_page_config(page_title="AI SDLC Wizard", layout="wide")
st.title("🧠 AI-Powered SDLC Workflow Wizard")

# Initialize session state
if "thread" not in st.session_state:
    import uuid
    st.session_state.thread = {"configurable": {"thread_id": str(uuid.uuid4())}}
    st.session_state.state = {
        "requirements": "",
        "user_stories": [],
        "user_story_status": "Approve",
        "user_story_feedback": [],
        "design_document": {},
        "design_document_review_status": "Approve",
        "design_document_review_feedback": [],
        "code": "",
        "code_review_status": "Approve",
        "code_review_feedback": [],
        "security_review_status": "Approve",
        "security_review_feedback": "",
        "test_cases": "",
        "test_cases_review_status": "Approve",
        "test_cases_review_feedback": [],
        "qa_review_status": "Approve",
        "qa_review_feedback": [],
        "deployment": ""
    }
    st.session_state.active_node = "User Requirements"
    st.session_state.events = []

# Display visual progress tracker
flow_order = [
    "User Requirements",
    "Auto-generate User Stories",
    "Human User Story Approval",
    "Create Design Document",
    "Human Design Document Review",
    "Generate Code",
    "Human Code Review",
    "Security Review",
    "Human Security Review",
    "Write Test Cases",
    "Human Test Cases Review",
    "QA Testing",
    "Human QA Review",
    "Deployment"
]

def progress_badge(node):
    current = st.session_state.active_node
    if current not in flow_order:
        return "🔘"  # unknown or system node like __interrupt__

    if flow_order.index(node) < flow_order.index(current):
        return "🟢"
    elif node == current:
        return "🟡"
    else:
        return "⚪"

st.markdown("""## 🔄 SDLC Progress Tracker""")

st.markdown(" → ".join(f"{progress_badge(n)} {n}" for n in flow_order))

# Tab-based layout
tabs = st.tabs(["User Requirements", "User Stories", "Design Document", "Code", "Test Cases", "Security", "QA", "Deployment"])
state = st.session_state.state

with tabs[0]:
    st.header("📋 User Requirements")
    requirements = st.text_area("Enter Requirements:", state.get("requirements", ""), key="requirements_input")
    if st.button("Submit Requirements", key="requirements_submit"):
        # Update state with new requirements
        state['requirements'] = requirements
        st.session_state.state = state
        
        # Start the graph stream
        for event in graph.stream(state, st.session_state.thread):
            st.session_state.events.append(event)
            for node, output in event.items():
                if isinstance(output, dict):
                    st.session_state.state.update(output)
                st.session_state.active_node = node
        st.rerun()


with tabs[1]:
    st.header("📘 User Stories")
    # Display user stories
    user_stories = st.session_state.state.get("user_stories", [])
    for i, story in enumerate(user_stories, 1):
        st.markdown(f"**{i}.** {story}")
    
    # Show approval UI if we have user stories
    if user_stories:
        status = st.radio("Approve the User Stories?", ["Approve", "Denied"], key="user_stories_approval")
        feedback = st.text_area("Feedback (if denied):", key="user_stories_feedback")
        if st.button("Continue from User Story Review", key="user_stories_continue"):
            # Update state with review decision
            graph.update_state(
                st.session_state.thread,
                {"user_story_status": status, "user_story_feedback": [feedback]},
                as_node="Human User Story Approval"
            )
            # Continue graph execution
            for event in graph.stream(None, st.session_state.thread):
                st.session_state.events.append(event)
                for node, output in event.items():
                    if isinstance(output, dict):
                        st.session_state.state.update(output)
                    st.session_state.active_node = node
            st.rerun()

with tabs[2]:
    st.header("📐 Design Document")
    doc = st.session_state.state.get("design_document", {})
    
    # Display design document sections
    sections = ["functional", "technical", "assumptions", "open_questions"]
    has_content = False
    
    # Check if doc is a dictionary and has content
    if isinstance(doc, dict):
        # Display each section
        for section in sections:
            if section in doc and isinstance(doc[section], list):
                items = doc[section]
                if items:
                    has_content = True
                    st.subheader(section.replace("_", " ").title())
                    for item in items:
                        st.markdown(f"- {item}")
    
    # Show approval UI if we have design document content
    if has_content:
        status = st.radio("Approve the Design Document?", ["Approve", "Denied"], key="design_doc_approval")
        feedback = st.text_area("Feedback (if denied):", key="design_doc_feedback")
        if st.button("Continue from Design Document Review", key="design_doc_continue"):
            graph.update_state(
                st.session_state.thread,
                {"design_document_review_status": status, "design_document_review_feedback": [feedback]},
                as_node="Human Design Document Review"
            )
            for event in graph.stream(None, st.session_state.thread):
                st.session_state.events.append(event)
                for node, output in event.items():
                    if isinstance(output, dict):
                        st.session_state.state.update(output)
                    st.session_state.active_node = node
            st.rerun()

with tabs[3]:
    st.header("💻 Generated Code")
    code = st.session_state.state.get("code", "No code generated yet.")
    st.code(code)
    
    # Show approval UI if we have code
    if code and code != "No code generated yet.":
        status = st.radio("Approve the Code?", ["Approve", "Denied"], key="code_approval")
        feedback = st.text_area("Feedback (if denied):", key="code_feedback")
        if st.button("Continue from Code Review", key="code_continue"):
            graph.update_state(
                st.session_state.thread,
                {"code_review_status": status, "code_review_feedback": [feedback]},
                as_node="Human Code Review"
            )
            for event in graph.stream(None, st.session_state.thread):
                st.session_state.events.append(event)
                for node, output in event.items():
                    if isinstance(output, dict):
                        st.session_state.state.update(output)
                    st.session_state.active_node = node
            st.rerun()

with tabs[4]:
    st.header("🧪 Test Cases")
    test_cases = st.session_state.state.get("test_cases", "No test cases yet.")
    st.text_area("Test Cases:", test_cases, height=300, key="test_cases_display")
    
    # Show approval UI if we have test cases
    if test_cases and test_cases != "No test cases yet.":
        status = st.radio("Approve the Test Cases?", ["Approve", "Denied"], key="test_cases_approval")
        feedback = st.text_area("Feedback (if denied):", key="test_cases_feedback")
        if st.button("Continue from Test Case Review", key="test_cases_continue"):
            graph.update_state(
                st.session_state.thread,
                {"test_cases_review_status": status, "test_cases_review_feedback": [feedback]},
                as_node="Human Test Cases Review"
            )
            for event in graph.stream(None, st.session_state.thread):
                st.session_state.events.append(event)
                for node, output in event.items():
                    if isinstance(output, dict):
                        st.session_state.state.update(output)
                    st.session_state.active_node = node
            st.rerun()

with tabs[5]:
    st.header("🔒 Security Review")
    st.write("**Security Feedback:**")
    security_feedback = st.session_state.state.get("security_review_feedback", "N/A")
    st.markdown(security_feedback)
    
    # Show approval UI if we have security feedback
    if security_feedback and security_feedback != "N/A":
        status = st.radio("Approve Security Review?", ["Approve", "Denied"], key="security_approval")
        security_feedback_text = st.text_area("Feedback (if denied):", key="security_feedback")
        if st.button("Continue from Security Review", key="security_continue"):
            graph.update_state(
                st.session_state.thread,
                {"security_review_status": status, "security_feedback": security_feedback_text},
                as_node="Human Security Review"
            )
            for event in graph.stream(None, st.session_state.thread):
                st.session_state.events.append(event)
                for node, output in event.items():
                    if isinstance(output, dict):
                        st.session_state.state.update(output)
                    st.session_state.active_node = node
            st.rerun()

with tabs[6]:
    st.header("✅ QA Review")
    st.write("**QA Feedback:**")
    qa_feedback = st.session_state.state.get("qa_review_feedback", [])
    if isinstance(qa_feedback, list):
        # Join list items with newlines
        feedback_text = "\n".join(qa_feedback)
    else:
        # If it's a single string, use it directly
        feedback_text = qa_feedback
    # Replace any extra spaces between characters
    feedback_text = ' '.join(feedback_text.split())
    st.markdown(feedback_text)
    
    # Show approval UI if we have QA feedback
    if qa_feedback:
        status = st.radio("Approve QA Testing?", ["Approve", "Denied"], key="qa_approval_1")
        feedback = st.text_area("Feedback (if denied):", key="qa_feedback_1")
        if st.button("Continue from QA Review", key="qa_continue_1"):
            graph.update_state(
                st.session_state.thread,
                {"qa_review_status": status, "qa_review_feedback": [feedback]},
                as_node="Human QA Review"
            )
            for event in graph.stream(None, st.session_state.thread):
                st.session_state.events.append(event)
                for node, output in event.items():
                    if isinstance(output, dict):
                        st.session_state.state.update(output)
                    st.session_state.active_node = node
            st.rerun()

with tabs[7]:
    st.header("🚀 Deployment")
    if state.get("deployment"):
        st.success("Application successfully deployed!")
    else:
        st.warning("Not yet deployed. Complete QA to trigger deployment.")
