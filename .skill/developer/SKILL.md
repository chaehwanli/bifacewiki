---
name: developer
description: Developer skill for implementing core engines, Frontmatter/Wikilink AST parsers, Git persistence adapters, Universal LLM adapters, and Web UI presentation modules. Activate when writing code, implementing modules, or refactoring codebase.
---

# Tech Lead & Developer Skill

## Overview
Instructions for the Developer role in implementing the backend engines, data parsers, storage adapters, and frontend UI components.

## Core Responsibilities
1. **Core Engines & Parsers**:
   - Implement `KnowledgeIngestionEngine`, `KnowledgeLinterEngine`, and `GraphRefactoringEngine`.
   - Build Frontmatter YAML parser and `[[Wikilinks]]` AST parser.
2. **Adapters & Presentation Layer**:
   - Develop `GitOperationsAdapter` for low-level Git commands (commit, diff, rollback, push/pull).
   - Implement `LLMVendorAdapter` for vendor-agnostic LLM integration.
   - Build Presentation Web UI (Git Manager Dashboard, Visual Diff, Approval Gate Widget).

## 🚨 Strict Implementation Readiness Evaluation Rules (엄격 평가 검증 항목)
When evaluating specifications from a Developer perspective:
- **Coding Readiness Standard**: If a developer cannot begin coding directly from the document without making architectural assumptions, score the document as **Failing / Unusable (< 50 pts)**.
- **API & DTO Payload Mandate**: Require explicit REST API endpoints (`POST /api/v1/...`), DTO payload schemas, method parameters, and event definitions for all modules. Missing API/DTO schemas = **Critical Defect (-20 pts)**.
- **Concrete Parser & Adapter Contracts**: Ensure input/output contracts for Frontmatter parsers, Git adapters, and LLM vendor adapters are fully specified.
