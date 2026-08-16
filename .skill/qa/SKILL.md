---
name: qa
description: QA skill for designing and executing unit, integration, contract, and NFR performance/security verification test cases mapped to REQ-DSGN-TEST matrix. Activate when writing test cases, testing software, or auditing quality metrics.
---

# QA & Functional Test Skill

## Overview
Instructions for the QA Lead & Functional Test Team role in verifying system functionality, API contracts, traceability, and NFR benchmarks.

## Core Responsibilities
1. **Traceability-based Test Case Design**:
   - Design test scenarios mapped directly to `REQ-DSGN-TEST` identifiers in `0816_requirements_and_nfr_spec.md`.
2. **Contract & Mock Testing**:
   - Build test stubs for LLM Tool Calling (`knowledge_search`, `knowledge_retrieve`).
   - Validate that `KnowledgeRetrievalSkill` strictly filters out non-production nodes unless specified.
3. **NFR Benchmark Verification**:
   - Benchmark ingestion latency `< 3s`, Ref-DAG parsing `< 1s` (1k docs), Git commit `< 500ms`.
   - Verify local LLM (Ollama) localhost data isolation.

## 🚨 Strict Testability & Traceability Evaluation Rules (엄격 평가 검증 항목)
When evaluating specifications from a QA/Tester perspective:
- **`DSGN` Traceability Mandate**: Verify that formal `DSGN-xxx` module tags from requirements specs are explicitly annotated in the architecture module tables. Missing tags = **Traceability Defect (-5 pts)**.
- **Contract Testing Feasibility**: Require explicit API schemas and Event contracts. If absent, flag the system as **Untestable (Contract Mocking Impossible) (-15 pts)**.
- **Verifiable NFR Target Points**: Ensure performance benchmarks (< 3s, < 1s, < 500ms) and security isolation boundaries have designated architectural endpoints for test instrumentation.
