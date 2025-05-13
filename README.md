# Automated SDLC Agentic AI Workflow with Langgraph and Human-in-the-loop

This project implements an Agentic AI-powered Software Development Lifecycle (SDLC) workflow using LangGraph, ChatGroq, and optional Human-in-the-Loop (HITL) decision points.

It enables fully or semi-autonomous generation of user stories, design documents, production-grade Python code, test cases, security reviews, QA validation, and deployment—all orchestrated through a dynamic state graph.
 
 
# Key Features
- End-to-End SDLC Automation: From requirements gathering to deployment
- LangGraph Orchestration: Modular state graph with interruptible human decision points
- LLM-Powered Generation: Uses Groq + Gemma LLM to produce structured artifacts
- Human-in-the-Loop Support: Manual approvals at every critical gate (design, code, security, QA)
- Artifact Exporting: Outputs user stories, design docs (.docx), Python code files, and test cases


# Architecture
This system uses a LangGraph-based state machine to automate and govern the Software Development Lifecycle with optional human checkpoints before critical decisions.


# Workflow Overview
Each stage represents an autonomous or human-in-the-loop process, controlled by LangGraph, with conditional transitions (Approve, Denied) for regenerating outputs or progressing forward.

![SDLC Agentic AI Workflow](assets/sdlc_flow.png)



# SDLC Stages & Logic
|Stage	| Description |
| --- | --- |
| User Requirements | Accepts raw requirements from user input |
| Auto-generate Stories | Generates 6 Agile-format user stories using LLM |
| Design Document	Creates | Functional & Technical Design in structured format |
| Code Generation | Produces modular, secure Python code with multi-file output |
| Security Review | Audits code for vulnerabilities and best practices |
| Test Case Generation | Writes QA test cases based on code and requirements |
| QA Review | Simulates QA test runs and validates test coverage |
| Deployment | Final stage if QA is approved |


# Artifacts Produced
| Artifact Type   | Format      | Location                         |
| --------------- | ----------- | -------------------------------- |
| User Stories    | `.txt`      | `artifacts/user_stories.txt`     |
| Design Document | `.docx`     | `artifacts/design_document.docx` |
| Generated Code  | `.py files` | `generated_code/`                |
| Test Cases      | `.txt`      | `test_cases/`                    |


# Review & Feedback Handling
Each review stage (Stories, Design, Code, Security, QA) supports:

✅ Approve: Progresses to next stage
❌ Denied: Triggers regeneration with updated feedback context

HITL checkpoints are configured via **interrupt_before**, making the graph resumable with user interaction.

# LLM Prompt Engineering
Prompts are customized to:

Enforce code quality (SRP, docstrings, comments)
Split logic into files like api.py, models.py, services.py
Require structured outputs with validation-ready format
Emphasize security best practices

LLM used: ChatGroq(model="gemma2-9b-it")



# Getting Started
**1. Clone and Install Dependencies**
```python
git clone https://github.com/your-username/agentic-sdlc-graph.git
cd agentic-sdlc-graph
pip install -r requirements.txt
```

**2. Set Environment Variables**
Create a .env file:
```python
GROQ_API_KEY=your_groq_api_key
```

**3. Run Streamlit UI**
```python
streamlit run streamlit_app.py
```

# Tech Stack
| Layer	| Technology |
| --- | --- |
| LLM	| ChatGroq using Gemma |
| Orchestration	| LangGraph |
| UI	| Streamlit |
| State Checkpointing	| In-memory via MemorySaver (can be extended to Redis, DB) |


# Security Considerations
- Regenerates insecure code based on Security Review Feedback
- Enforces input sanitization, auth, access controls in prompts
- Validates human review before deployment


# Future Enhancements
- Monitoring and alerting stage (coming soon)
- Support for non-Python code generation (multi-language)
- Redis or Mongo-based graph checkpointing
- CI/CD pipeline integration with GitHub Actions
