---
name: architect
description: System Architect skill for designing overall Knowledge Platform architecture, Ref-DAG modeling, module interfaces, sequence flows, and NFR constraints. Activate when performing architectural design, specification writing, or structural refactoring.
---

# System Architect Skill

## Overview
Instructions for the System Architect role in defining, maintaining, and auditing system architecture specs in `.doc/0816_knowledge_platform_architecture_spec.md`.

## Core Responsibilities
1. **Architecture & Ref-DAG Modeling**:
   - Define Dual-Layer architecture (Physical Git store + Logical Ref-DAG graph).
   - Ensure Directed Acyclic Graph (DAG) constraints and Kahn's / DFS cycle prevention algorithms.
2. **Interface & Sequence Specification**:
   - Define `DSGN-xxx` module boundaries and mapping.
   - Specify REST API contracts (`POST /api/v1/...`) and Mermaid Sequence Diagrams for dynamic flows.
3. **NFR Constraints & Security Isolation**:
   - Design `status: production` context isolation to prevent Model Collapse (`NFR-SEC-01`).
   - Define In-Memory index invalidation triggers (Git hooks / file change events).

## 🚨 Strict Architecture Evaluation Rules (엄격 평가 검증 항목)
When evaluating or auditing architecture specifications, apply the following strict criteria:
- **Reject Outline-Only Documents**: Do NOT award passing scores (> 60) to high-level conceptual outlines that lack runtime implementation details.
- **Dynamic Sequence Flow Requirement**: If Mermaid Sequence Diagrams for core runtime flows (Ingestion -> Linter -> Approval Gate -> Git Commit) are missing, flag as **Major Defect (-15 pts)**.
- **NFR Implementation Mechanism**: Verify explicit architectural mechanisms for `status: production` context filtering, cache invalidation, and localhost security proxy boundaries.
- **Algorithm & State Specifications**: Require explicit mention of Ref-DAG cycle detection (Kahn's/DFS) and index invalidation triggers.
