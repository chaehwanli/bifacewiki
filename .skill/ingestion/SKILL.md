---
name: ingestion
description: Knowledge Ingestion Engine skill for parsing Q&A conversations, extracting Atomic Markdown documents, validating minimal schema, classifying negative knowledge, and writing draft files. Activate when implementing DSGN-CORE-INGEST or executing knowledge extraction tools.
---

# Knowledge Ingestion Engine Skill (`DSGN-CORE-INGEST`)

## Overview
Instructions and domain rules for implementing and utilizing the **Knowledge Ingestion Engine** (`DSGN-CORE-INGEST`).

## Core Responsibilities & Specifications
1. **Q&A Conversation Ingestion (`UC-001`)**:
   - Parse multi-turn Q&A conversation logs (`KnowledgeExtractRequestDTO`).
   - Distinguish positive solutions (`type: solution`) and negative knowledge/anti-patterns (`type: negative_knowledge`).
   - Extract raw text into a single **Atomic Markdown Document** (`NFR-MAINT-02`).
2. **Minimal Frontmatter Schema Validation**:
   - Ensure required fields: `id`, `title`, `type`, `status` (`draft`), `author_type` (`ai_generated` or `human_authored`).
3. **Draft File System Persistence**:
   - Save extracted document to `.drafts/<node-id>.md`.
   - Send change notification to `RefDAGIndexerEngine`.

## Key Interfaces & DTO Schemas
- **Method**: `extract_from_conversation(session_log: str, hints: List[str]) -> IngestionResultDTO`
- **Method**: `parse_frontmatter_schema(raw_md: str) -> FrontmatterDTO`
- **Method**: `validate_atomic_constraint(content: str) -> bool`
- **REST Endpoint**: `POST /api/v1/knowledge/extract`
- **LLM Agent Tool**: `knowledge_extract`

## 🚨 Strict Implementation & Quality Rules
- **Latency Requirement (`NFR-PERF-01`)**: Extraction & draft saving must finish within **< 3 seconds**.
- **Atomic Requirement (`NFR-MAINT-02`)**: One document MUST contain only one atomic topic. Split multi-topic conversations into multiple nodes.
- **Initial State Constraint**: All AI-extracted nodes MUST have `status: draft` and be placed in `.drafts/`. Never directly write to `knowledge/` (`NFR-SEC-01`).
