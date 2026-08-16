---
name: agent_binder
description: Skill for implementing Universal LLM Vendor Adapter (DSGN-LLM-ADAPTER), Skill Binding Middleware (DSGN-AGENT-BINDER), and Knowledge Retrieval Skill (DSGN-AGENT-SKILL), including Localhost Ollama proxy isolation (NFR-SEC-03). Activate when implementing LLM vendor integrations or agent tool binding.
---

# Universal LLM Adapter & Agent Binding Skill (`DSGN-LLM-ADAPTER`, `DSGN-AGENT-BINDER`, `DSGN-AGENT-SKILL`)

## Overview
Instructions and domain rules for implementing the **Agent & Integration Layer** modules.

## Core Responsibilities & Specifications
1. **Universal LLM Vendor Adapter (`DSGN-LLM-ADAPTER`, `UC-005`)**:
   - Abstract OpenAI GPT, Gemini, Claude, and Local Ollama behind a unified interface.
   - Localhost Proxy Sandbox (`NFR-SEC-03`): Route Ollama traffic exclusively via `http://127.0.0.1:11434` with zero external network access.
2. **Skill Binding Middleware (`DSGN-AGENT-BINDER`, `UC-006`)**:
   - Read `.agent/skills/` Frontmatter and Tool Schemas.
   - Inject system prompts and function calling tool definitions into LLM sessions dynamically.
3. **Knowledge Retrieval Skill (`DSGN-AGENT-SKILL`, `UC-007`)**:
   - Execute `knowledge_search()`, `knowledge_retrieve()`, and `knowledge_context_inject()`.
   - Traverse Ref-DAG index and assemble high-precision markdown context strings for LLM injection.

## Key Interfaces & REST Endpoints
- **Method**: `invoke(request: LLMInvokeRequestDTO) -> LLMInvokeResponseDTO`
- **Method**: `switch_vendor(vendor_code: str, config: VendorConfigDTO) -> bool`
- **Method**: `bind_skill(session_id: str, preset_id: str) -> BoundSessionDTO`
- **Method**: `knowledge_search(query: str, filter_tags: List[str]) -> List[NodeSummaryDTO]`
- **Method**: `knowledge_retrieve(node_id: str, depth: int) -> KnowledgeContextDTO`
- **Method**: `knowledge_context_inject(context: KnowledgeContextDTO) -> str`
- **REST Endpoints**: `PUT /api/v1/settings/llm-vendor`, `POST /api/v1/agent/bind-skill`
- **LLM Agent Tools**: `agent_bind_skill`, `knowledge_search`, `knowledge_retrieve`, `knowledge_context_inject`

## 🚨 Strict Implementation & Quality Rules
- **One-Click Binding Latency (`NFR-PERF-04`)**: Skill binding must complete in **< 200ms**.
- **Context Injection Latency (`NFR-PERF-05`)**: Knowledge search & context assembly must complete in **< 500ms**.
- **Zero Hallucination Context**: Injected context MUST be restricted strictly to `status: production` nodes (`NFR-SEC-01`).
