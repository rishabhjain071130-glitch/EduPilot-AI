# 🎓 EduPilot AI: System & Agent Architecture Design

Welcome to the **EduPilot AI** system architecture manual. This document describes the modular architecture, multi-agent cooperative pattern, security design, and production deployment layout for the EduPilot AI platform.

---

## 🏗️ 1. System Architecture

EduPilot AI uses a decoupled multi-tier architecture to separate presentation, orchestration, domain logic, and external LLM services.

```mermaid
graph TD
    User([Student / User]) <--> Streamlit[[app.py Frontend UI]]
    Streamlit <--> Orchestrator[[master_agent.py Orchestration]]
    Orchestrator <--> Security[[security.py Validation Layer]]
    Orchestrator <--> LLM[Google Gemini 2.5 API]
    Orchestrator <--> MCPClient[MCP Client Runtime]
    MCPClient <--> MCPServer[[server.py FastMCP Server]]
    MCPServer <--> Data[(In-Memory Educational Database)]
```

### Component Details
* **Frontend Web UI ([app.py](file:///C:/Users/Lenovo/EduPilot-AI/frontend/app.py))**: Handles user input parameters, maintains Streamlit session states, and renders visual roadmaps and study schedules.
* **Orchestrator ([master_agent.py](file:///C:/Users/Lenovo/EduPilot-AI/agents/master_agent.py))**: Coordinates control loops and aggregates data returned by the independent AI agents.
* **Security & Guardrail Layer ([security.py](file:///C:/Users/Lenovo/EduPilot-AI/agents/security.py))**: Evaluates incoming query syntax for malicious prompt injection before execution.
* **MCP Tool Server ([server.py](file:///C:/Users/Lenovo/EduPilot-AI/mcp/server.py))**: Standardized FastMCP microservice providing career and study data.
* **Gemini Client ([gemini_client.py](file:///C:/Users/Lenovo/EduPilot-AI/agents/gemini_client.py))**: Standardized SDK integration managing connection parameters, models list, and retry backoffs.

---

## 🤖 2. Agent Architecture

The application adopts a **Cooperative Multi-Agent Pattern**. Specialized sub-agents perform analysis on a specific domain using dedicated prompt policies.

```mermaid
graph LR
    Master[[master_agent.py]] --> ProfileAgent[[profile_agent.py]]
    Master --> CareerAgent[[career_agent.py]]
    Master --> StudyAgent[[study_agent.py]]
    Master --> ResumeAgent[[resume_agent.py]]
```

### Agent Directory
* **Profile Agent ([profile_agent.py](file:///C:/Users/Lenovo/EduPilot-AI/agents/profile_agent.py))**: Conducts SWOT analysis, identifies academic milestones, and highlights student skill gaps.
* **Career Agent ([career_agent.py](file:///C:/Users/Lenovo/EduPilot-AI/agents/career_agent.py))**: Maps out long-term milestones, targets certification paths, and recommends projects.
* **Study Agent ([study_agent.py](file:///C:/Users/Lenovo/EduPilot-AI/agents/study_agent.py))**: Structures structured study routines, revision schedules, and time blocks.
* **Resume Agent ([resume_agent.py](file:///C:/Users/Lenovo/EduPilot-AI/agents/resume_agent.py))**: Focuses on professional resumes, formatting corrections, and impact statements.

---

## 🔄 3. Data Flow Architecture

The sequence below details the lifecycle of a student request from input transmission to dashboard rendering:

```mermaid
sequenceDiagram
    autonumber
    actor Student as Student (User)
    participant App as Streamlit Frontend (app.py)
    participant Sec as Security Validator (security.py)
    participant Master as Master Agent (master_agent.py)
    participant Gemini as Gemini API Client
    participant MCP as MCP Server (server.py)

    Student->>App: Input Student Details
    App->>Sec: Invoke validate_input()
    alt Safety Violation Detected
        Sec-->>App: Validation Failed (Flagged Input)
        App-->>Student: Display Error Notification
    else Input Approved
        Sec-->>App: Validation Succeeded
        App->>Master: Send Details Payload
        Note over Master: Orchestrator spawns analysis loop
        Master->>Gemini: Run profile_agent Prompt
        Gemini-->>Master: Return Profile Analysis
        Master->>Gemini: Run career_agent Prompt (Uses MCP Tools)
        Gemini->>MCP: Query career_advice(interest)
        MCP-->>Gemini: Return Career Path JSON Details
        Gemini-->>Master: Return Final Career Roadmap
        Master->>Gemini: Run study_agent & resume_agent prompts
        Gemini-->>Master: Return Study Routine & Resume suggestions
        Master->>Master: Synthesize and format report
        Master-->>App: Return Completed Career Markdown Report
        App-->>Student: Display Interactive Report Dashboards
    end
```

---

## 🛡️ 4. Security Layer Design

EduPilot AI uses a **Defense-in-Depth** model to intercept malicious inputs, protecting system credentials and core agent prompts.

```mermaid
flowchart TD
    RawInput[User Input Details] --> Guard1[1. Input Length & Character Validation]
    Guard1 --> Guard2[2. Blacklist Pattern Matcher]
    Guard2 -- Match Detected --> Reject[Raise SafetyException & Block Call]
    Guard2 -- Clear --> Guard3[3. Model-Based Jailbreak Scanner]
    Guard3 -- Flagged Injection --> Reject
    Guard3 -- Approved --> Pipeline[4. Forward to Agent Pipeline]
```

### Key Security Policies
1. **Keyword Sanitization**: The [`validate_input`](file:///C:/Users/Lenovo/EduPilot-AI/agents/security.py#L1-L13) utility acts as the first line of defense, filtering keywords that match common injection phrases (e.g. `ignore instructions`, `show api key`).
2. **Context Isolation**: System instructions are defined programmatically. Student input is treated strictly as data parameters inside isolated prompts.
3. **Environment Encapsulation**: Credentials, including `GEMINI_API_KEY`, are managed as read-only variables in host environments, never exposed in client sessions or output screens.

---

## 🌐 5. Deployment Architecture

For scalable production workloads, the application utilizes a serverless, containerized cluster topology.

```mermaid
graph TD
    DNS[Route 53 / Cloud DNS] --> LB[Application Load Balancer]
    LB --> WebService[ECS Fargate: Streamlit Web UI Instance]
    WebService --> MCPAgent[ECS Fargate: MCP Server Instance]
    WebService --> GeminiAPI[Google Gemini Gateway]
    WebService --> Redis[(ElastiCache Redis: Session Store)]
```

### Production Infrastructure Highlights
* **Orchestration**: Web and MCP servers run as independent, autoscaling **Docker Containers** using AWS ECS Fargate or Google Cloud Run.
* **Caching**: **Redis** cluster manages session memory and caches redundant LLM responses to reduce API billing.
* **Secrets Management**: Secrets are injected during container startup from **AWS Secrets Manager**, preventing key exposure in repository check-ins.
