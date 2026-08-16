---
name: linter_engine
description: Knowledge Linter Engine skill for 24/7 background static auditing of broken links, orphan nodes, YAML schema errors, 180-day stale node detection, and contradiction detection. Activate when implementing DSGN-LINTER-ENGINE or running audit scans.
---

# Knowledge Linter Engine Skill (`DSGN-LINTER-ENGINE`)

## Overview
Instructions and domain rules for implementing and running the **Knowledge Linter Engine** (`DSGN-LINTER-ENGINE`).

## Core Responsibilities & Specifications
1. **24/7 Static Audit Scanning (`UC-008`)**:
   - Detect Broken Links: `[[Wikilinks]]` pointing to missing file/heading nodes.
   - Detect Orphan Nodes: Nodes with zero incoming and zero outgoing reference edges.
   - Detect Schema Violations: Invalid or missing required YAML frontmatter metadata.
   - Detect Stale Nodes: Nodes un-updated for `> 180 days`.
   - Detect Contradictions: Conflicting claims across nodes via semantic check.
2. **Audit Report Generation**:
   - Compile findings into `LintAuditReportDTO` (`lint_report.json`).
   - Publish audit reports to Approval & Audit Dashboard (`DSGN-APPROVAL-GATE`).

## Key Interfaces & REST Endpoints
- **Method**: `run_audit_scan(repo_path: str) -> LintAuditReportDTO`
- **Method**: `detect_broken_links(graph: RefDAGGraph) -> List[BrokenLinkIssue]`
- **Method**: `detect_orphan_nodes(graph: RefDAGGraph) -> List[str]`
- **REST Endpoint**: `POST /api/v1/audit/lint`
- **LLM Agent Tool**: `knowledge_audit_scan`

## 🚨 Strict Implementation & Quality Rules
- **Non-Destructive Scanning**: Scanning MUST be read-only and static; it must never mutate underlying markdown files directly.
- **Audit Verification (`NFR-RELI-02`)**: Audit reports must be generated seamlessly without blocking graph indexing or file watcher operations.
