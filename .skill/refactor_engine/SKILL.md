---
name: refactor_engine
description: Graph Refactoring Engine skill for proposing duplicate node merge plans (similarity >= 0.90), executing auto-redirection for Wikilinks, and pruning/archiving stale nodes across the lifecycle. Activate when implementing DSGN-REFACTOR-ENGINE or executing graph refactoring tasks.
---

# Graph Refactoring Engine Skill (`DSGN-REFACTOR-ENGINE`)

## Overview
Instructions and domain rules for implementing and managing the **Graph Refactoring Engine** (`DSGN-REFACTOR-ENGINE`).

## Core Responsibilities & Specifications
1. **Duplicate Node Consolidation (`UC-010`)**:
   - Identify candidate fragmented nodes with semantic similarity $\ge 0.90$.
   - Formulate `RefactorPlanDTO` proposing node merge.
2. **Wikilink Auto-Redirection**:
   - Update all referencing `[[Wikilinks]]` in active markdown files to point to the merged target node.
3. **Lifecycle Archiving & Pruning**:
   - Transition deprecated nodes from `knowledge/` to `archive/deprecated/` or `archive/expired/`.
   - Maintain historical backward compatibility.

## Key Interfaces & REST Endpoints
- **Method**: `propose_merge_plan(candidate_ids: List[str]) -> RefactorPlanDTO`
- **Method**: `execute_merge(plan_id: str) -> MergeResultDTO`
- **Method**: `prune_deprecated_nodes(target_ids: List[str]) -> PruneResultDTO`
- **REST Endpoints**: `POST /api/v1/refactor/merge`, `POST /api/v1/refactor/prune`
- **LLM Agent Tool**: `knowledge_propose_merge` (Plan formulation only)

## 🚨 Strict Implementation & Quality Rules
- **Human Approval Requirement**: Execution (`execute_merge`) MUST be triggered only after human review/approval of the refactor plan.
- **Atomic Integrity (`NFR-MAINT-02`)**: Merged nodes must maintain single atomic topic focus without schema corruptions.
