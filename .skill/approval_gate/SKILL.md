---
name: approval_gate
description: Human Approval Gate Manager skill for managing human brokerage decision queues, enforcing Model Collapse prevention (NFR-SEC-01), directory isolation (.drafts/), and promoting approved knowledge to production. Activate when implementing DSGN-APPROVAL-GATE or managing approval workflows.
---

# Human Approval Gate Manager Skill (`DSGN-APPROVAL-GATE`)

## Overview
Instructions and domain rules for implementing the **Human Approval Gate Manager** (`DSGN-APPROVAL-GATE`).

## Core Responsibilities & Specifications
1. **Model Collapse Prevention Architecture (`NFR-SEC-01`)**:
   - Isolate AI-generated knowledge (`author_type: ai_generated`) in `.drafts/` with `status: draft`.
   - Prevent draft nodes from being indexed in production search or injected into LLM sessions.
2. **Human Brokerage Review & Decision (`UC-009`)**:
   - Serve pending draft queue with visual diffs and Linter Audit reports.
   - Process Human Broker decisions: `approve`, `reject`, `request_revision`.
3. **Production Promotion & Commit**:
   - On `approve`: Move file from `.drafts/<node-id>.md` to `knowledge/<node-id>.md`, set `status: production`, annotate `approved_by`, and commit & merge into `main` branch.
   - Trigger graph reindexing (`RefDAGIndexerEngine.reindex_all()`).

## Key Interfaces & REST Endpoints
- **Method**: `get_pending_approvals() -> List[PendingApprovalNodeDTO]`
- **Method**: `decide_approval(decision_dto: ApprovalDecisionDTO) -> ApprovalResultDTO`
- **REST Endpoints**: `GET /api/v1/approval/pending`, `POST /api/v1/approval/decide`
- **LLM Agent Tools**: `knowledge_get_pending_approvals` (Read-Only queue inspection)

## 🚨 Strict Security & Authority Constraints
- **AI Self-Approval Prohibition (`NFR-SEC-01`)**: `decide_approval` API is **STRICTLY PROHIBITED** from being exposed as an LLM Tool! AI MUST NEVER approve its own draft nodes.
- **Human Authority Boundary**: Only human brokers via Web UI / authenticated REST API can execute node promotion.
