# EDITH — MCP-First Personal AI Assistant (Production-Ready Design)

## 1) Executive Overview
- **EDITH** is a **local-first, MCP-powered personal AI assistant** that performs real-world actions across communication, development, documents, and web navigation while keeping users in control.
- **Primary goal:** a **production-ready, exam-worthy** system that is secure, extensible, and usable by both technical and non-technical users.
- **Key pillars:** MCP-first design, hybrid (remote + local) MCP architecture, human-in-the-loop for sensitive actions, explicit consent for remote services, and dynamic MCP discovery.

---

## 2) High-Level Architecture Diagram (ASCII)
```
+-----------------------+           +------------------------------+
|     UI Layer          |           |      Remote MCP Servers      |
|  Web / Telegram / WA  |<--------->| Gmail / GitHub / Search /    |
+-----------+-----------+           | LinkedIn / Docs / Browser    |
            |                       +--------------+---------------+
            v                                      ^
+-----------------------+                          |
|   EDITH Orchestrator  |                          |
| - Intent Classifier   |                          |
| - Planner Agent       |                          |
| - Tool Router         |                          |
| - MCP Client          |<-------------------------+
| - Human Approval Gate |
| - Memory Manager      |                          +------------------+
+-----------+-----------+                          |   Local MCPs      |
            |                                      | OS / Editor / FS  |
            v                                      +------------------+
+-----------------------+
|  Config + Policy      |
|  (config.yaml)        |
+-----------------------+
```

---

## 3) Detailed Module Breakdown
### 3.1 EDITH Orchestrator
- **Responsibility:** central coordinator for all requests.
- **Inputs:** user message, session context, active policies, and available MCPs.
- **Outputs:** orchestrated plan, tool calls, and final response.

### 3.2 Intent Classifier
- **Responsibility:** detect intent categories (communication, dev, search, docs, web, chat).
- **Method:** lightweight LLM or rules + LLM fallback.
- **Outputs:** intent labels + confidence scores.

### 3.3 Planner Agent
- **Responsibility:** builds multi-step action plans using MCPs.
- **Features:**
  - selects MCPs dynamically
  - includes human approval checkpoints
  - retries with alternative MCPs if available

### 3.4 MCP Client
- **Responsibility:** discovery, invocation, and monitoring of MCP servers.
- **Capabilities:**
  - remote MCP registry
  - local MCP registry
  - health checks + timeouts
  - policy enforcement (local-first, privacy)

### 3.5 Tool Router
- **Responsibility:** maps planner steps to MCP calls.
- **Guarantees:**
  - no hard-coded integrations
  - dynamic endpoints
  - schema-aware input/output validation

### 3.6 Human Approval Gate
- **Responsibility:** pauses workflows for sensitive actions (login, captcha, payment, sending emails, posting content).
- **Policies:**
  - user confirmation required for any irreversible action
  - no bypass of security mechanisms

### 3.7 Memory Manager
- **Responsibility:** handles context memory and user preferences.
- **Storage:** local encrypted cache + optional remote memory opt-in.

### 3.8 UI Layer
- **Responsibility:** consistent UX across Web, Telegram, and WhatsApp.
- **All modes route to a single core API** for orchestration.

---

## 4) Folder Structure (Proposed)
```
/edith
  /core
    orchestrator.py
    intent_classifier.py
    planner.py
    tool_router.py
    mcp_client.py
    human_gate.py
    memory_manager.py
  /ui
    /web
    /telegram
    /whatsapp
  /mcp
    /local
    /remote
  /config
    config.yaml
  /docs
    architecture.md
    mcp_examples.md
    user_flows.md
  /scripts
    edith (CLI launcher)
```

---

## 4.1) Scaffold Status (What Exists in This Repo)
- A minimal Python package under `edith/` with orchestrator, planner, MCP client, and human gate stubs.
- A CLI launcher at `scripts/edith` implementing `./edith setup` via `python -m edith.cli`.
- A sample `config/config.yaml` used as a reference for local-first setup.
- `docs/architecture.md` with runtime flow and extension notes.

---

## 5) Core System Prompts (Representative)
### 5.1 Orchestrator System Prompt
```
You are EDITH, a local-first MCP-powered assistant.
Rules:
- Prefer remote MCPs unless a local MCP is explicitly required.
- Never bypass logins, captcha, or payments.
- For any sensitive action (send email, publish post, execute OS action), require user approval.
- Always summarize tool outputs and provide transparent reasoning.
```

### 5.2 Human Approval Gate Prompt
```
This action requires user approval. Explain the action clearly and wait for confirmation before proceeding.
```

---

## 6) Example MCP Calls (Conceptual)
### 6.1 Gmail MCP — List Unread Emails
```json
{
  "server": "gmail-mcp-remote",
  "action": "list_unread",
  "params": { "limit": 10 }
}
```

### 6.2 LinkedIn MCP — Create Post
```json
{
  "server": "linkedin-mcp-remote",
  "action": "create_text_post",
  "params": {
    "content": "Sharing a new update...",
    "visibility": "public"
  }
}
```

### 6.3 GitHub MCP — Clone Repo
```json
{
  "server": "github-mcp-remote",
  "action": "clone_repo",
  "params": {
    "url": "https://github.com/org/repo.git"
  }
}
```

### 6.4 Browser MCP — Extract Data
```json
{
  "server": "browser-mcp-remote",
  "action": "extract_structured",
  "params": {
    "url": "https://flipkart.com",
    "selector": "div.product-specs"
  }
}
```

---

## 7) Example User Flows
### 7.1 Gmail — Summarize Inbox
1. User: “Summarize my inbox.”
2. Orchestrator → Gmail MCP (remote).
3. Human Approval Gate? **No** (read-only).
4. MCP returns email list.
5. EDITH summarizes and returns results.

### 7.2 LinkedIn — Create Post
1. User: “Post this on LinkedIn.”
2. EDITH drafts post and requests approval.
3. User confirms.
4. LinkedIn MCP publishes post.
5. EDITH confirms completion.

### 7.3 Web Navigation — Flipkart Example
1. User: “Go to Flipkart and tell me available colors of Samsung S24 FE.”
2. EDITH opens Browser MCP (visible browser).
3. If login required → **pause** and ask user to login.
4. Extracts data and returns structured summary.

---

## 8) CLI-Based User Onboarding (Required)
### Command
```
./edith setup
```

### Flow
- Select **LLM provider** (OpenAI / Gemini / Groq).
- Select **model**.
- Enable MCP servers (remote + local).
- Enter API keys.
- Choose interaction modes (Web / Telegram / WhatsApp).
- OAuth authorization (browser-based).
- Save config to `config.yaml` locally.

---

## 9) Required Features Mapping
### Communication Assistant (Gmail)
- Read emails
- List unread emails
- Summarize inbox
- Draft + send emails
- **Remote Gmail MCP with OAuth**

### Professional Presence (LinkedIn)
- Create text posts
- Create media posts
- Rewrite posts (professional / casual / viral)
- **Remote MCP with browser automation fallback**

### Developer Assistant (GitHub)
- Clone repositories
- Open repo in selected editor (VS Code, Cursor, Android Studio)
- Explain repository structure
- **Remote GitHub MCP + Local OS/editor MCP**

### Live Search
- Triggered by “latest”, “today”, “now”, “price”, “news”
- **Remote Search MCP** with citation output

### Document Intelligence
- Support PDF, DOCX, PPT, XLSX, CSV, images
- Q&A, summarization, comparison, table extraction
- **Remote Document MCP** + local fallback for private files

### Web Navigation (Critical)
- Browser MCP for visible browsing, extraction, search
- **Pause for login / captcha / payment**

### Normal AI Chat
- ChatGPT-style reasoning, coding help, brainstorming

---

## 10) Final-Year Project Framing
### Problem Statement
Existing assistants are siloed, lack privacy controls, and hard-code integrations. There is a need for a secure, extensible, MCP-first assistant that can perform real-world actions while maintaining user oversight and local-first privacy.

### Objectives
- Build a modular MCP-first assistant that can orchestrate real-world tasks.
- Provide multi-channel access (Web, Telegram, WhatsApp).
- Implement safe human-in-the-loop workflows.
- Ensure privacy-first configuration and extensibility.

### Scope
- Communication (Gmail)
- Professional presence (LinkedIn)
- Developer assistant (GitHub)
- Document intelligence
- Web navigation automation
- Live search with citations

### Innovation / Novelty
- Hybrid MCP architecture (remote defaults + local extensions)
- Dynamic MCP discovery and routing
- Human-approval gate for sensitive actions
- Local-first privacy with explicit opt-in for remote services

---

## 11) Security & Ethics
- No credential harvesting
- No captcha bypass
- Explicit consent before sensitive actions
- Full transparency in actions taken

---

## 12) Extensibility Notes
- New MCP servers can be added via config without core logic changes.
- Each MCP server declares capabilities and schema for dynamic planning.
