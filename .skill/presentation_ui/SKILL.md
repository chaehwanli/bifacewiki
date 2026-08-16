---
name: presentation_ui
description: Presentation Layer skill for building Git Management Dashboard, Visual Line-by-Line Diff Viewer, Human Approval Gate Widget, LLM Vendor Selector, Edge Matrix Explorer, Search Playground, and External Launcher Adapter for Obsidian OS URI schemes (UC-001 ~ UC-011). Activate when building React Web UI, HTML Dashboard, or external protocol launchers.
---

# Presentation UI & External Launcher Skill (`DSGN-UI-DASHBOARD`, `DSGN-LAUNCHER-PROTOCOL`)

## Overview
Instructions, component rules, and REST API contracts for building the **Presentation Layer** web UI components (`src/ui/index.html`, `src/ui/git_management_dashboard.tsx`) and external launcher adapters (`ExternalLauncherAdapter`).

## Core UI Components & Use Case Specifications

1. **Git Management Dashboard & Visual Diff Viewer (`DSGN-UI-DASHBOARD`, `UC-004`, `UC-003`)**:
   - Provide visual Git repository status (Branch, Unstaged Count), Commit Timeline, and line-by-line Visual Diff Modal without CLI dependence.
   - Provide one-click `[Sync Remote]` (Push/Pull) and `[Rollback]` interface.
   - **REST Endpoints**: `GET /api/v1/git/status`, `GET /api/v1/git/history`, `GET /api/v1/git/diff`, `POST /api/v1/git/sync`, `POST /api/v1/git/rollback`

2. **LLM Vendor Switcher Widget (`DSGN-LLM-ADAPTER`, `UC-005`)**:
   - Render active LLM vendor selector dropdown in header (`OpenAI GPT-4o`, `Google Gemini 1.5 Pro`, `Anthropic Claude 3.5`, `Local Ollama`).
   - Enforce localhost proxy sandbox badge for local Ollama mode (`NFR-SEC-03`).
   - **REST Endpoints**: `GET /api/v1/settings/llm-vendor`, `PUT /api/v1/settings/llm-vendor`

3. **Ref-DAG Edge Matrix & Graph Explorer Widget (`DSGN-INDEXER-DAG`, `UC-002`, `UC-011`)**:
   - Render Active Nodes list and Edges Matrix table (`Source Node -> Target Node` directional dependency links).
   - Render `[Obsidian으로 직접 열기]` button per node triggering OS URI scheme (`obsidian://open?file=...`).
   - **REST Endpoints**: `GET /api/v1/graph/nodes`, `GET /api/v1/graph/edges`, `GET /api/v1/external/launch`

4. **Human Approval Gate Review Widget (`DSGN-APPROVAL-GATE`, `UC-009`)**:
   - Render draft review queue cards with side-by-side markdown comparison, `author_type: ai_generated` badge, and Linter audit results.
   - Provide explicit `[Approve & Merge]` and `[Reject]` buttons enforcing `NFR-SEC-01`.
   - **REST Endpoints**: `GET /api/v1/approval/pending`, `POST /api/v1/approval/decide`

5. **One-Click Skill Binding UI Widget (`DSGN-AGENT-BINDER`, `UC-006`)**:
   - Render preset skill binder cards (`qa_ingestion`, `knowledge_retrieval`, `linter_audit`, `refactor_merge`) for quick session prompt binding.
   - **REST Endpoint**: `POST /api/v1/agent/bind-skill`

6. **Knowledge Context Search Playground Widget (`DSGN-AGENT-SKILL`, `UC-007`)**:
   - Render user query test input box and `[Knowledge Context Inject Test]` button.
   - Display dynamically assembled Knowledge Context string and matched nodes.
   - **REST Endpoint**: `POST /api/v1/knowledge/search`

7. **Graph Refactoring & Lifecycle Control Widget (`DSGN-REFACTOR-ENGINE`, `UC-010`)**:
   - Render candidate node merge proposal card (`[Execute Merge Plan]`) and stale node archiving trigger button (`[Archive Stale Nodes]`).
   - **REST Endpoints**: `GET /api/v1/refactor/candidates`, `POST /api/v1/refactor/merge`, `POST /api/v1/refactor/prune`

## 🚨 Strict Design & Usability Rules
- **Non-Technical Usability**: Web UI must allow complete Git version management, vendor switching, and approval workflow without requiring CLI terminal execution.
- **Visual Clarity**: Clear badge indicators for node status (`draft`, `review_pending`, `production`, `deprecated`) and author type (`ai_generated`, `human`).
- **Response Latency**: Dashboard UI state updates must respond in **< 200ms**.
