---
name: indexer_dag
description: Ref-DAG Indexer Engine skill for parsing Frontmatter and [[Wikilinks]], building hierarchical node graphs (Primary & Sub-block), maintaining Tier-2 SQLite persistent cache, handling 500ms sliding window file watcher debouncing, and enforcing Kahn's algorithm cycle prevention. Activate when implementing DSGN-INDEXER-DAG or managing graph indexes.
---

# Ref-DAG In-Memory & Persistent Indexer Skill (`DSGN-INDEXER-DAG`)

## Overview
Instructions and domain rules for implementing and managing the **Ref-DAG In-Memory & Persistent Indexer Engine** (`DSGN-INDEXER-DAG`).

## Core Responsibilities & Specifications
1. **Ref-DAG Hierarchical Graph Modeling (`UC-002`)**:
   - Parse Frontmatter metadata and `[[Wikilinks]]` syntax.
   - Primary File Node ($V_{\text{file}}$) & Sub-block Node ($V_{\text{subblock}}$: `node-id#heading-slug`).
   - Directed Edge Types: `references`, `depends_on`, `parent_of`, `replaces`, `semantically_related`.
2. **2-Tier Persistent Graph Caching & Incremental Sync**:
   - Tier-1: Sub-millisecond (< 1ms) In-Memory Hot Graph.
   - Tier-2: Embedded SQLite persistent graph store (`nodes`, `edges`, `sub_blocks`).
   - Incremental Sync via `content_hash` comparison to achieve Cold Start **< 500ms** and Incremental Sync **< 50ms** (`NFR-PERF-02`).
3. **500ms Debounce Sliding Window Event Queue**:
   - `FileWatcherThrottler` buffers rapid file change events during bulk refactoring or git checkout.
   - Triggers `reindex_incremental()` only after 500ms quiet period.
4. **Kahn's Topological Sort Cycle Prevention**:
   - Validate proposed new edge $e = (u, v)$ against Primary and Sub-block nodes using Kahn's algorithm.
   - Raise `CircularDependencyException` if a cycle is detected (`NFR-RELI-03`).

## Key Interfaces & REST Endpoints
- **Method**: `reindex_incremental(changed_files: List[str]) -> RefDAGGraph`
- **Method**: `debounce_file_events(event_batch: List[FileEvent]) -> None`
- **Method**: `parse_sub_blocks(markdown_content: str, parent_id: str) -> List[SubBlockNode]`
- **Method**: `get_related_subgraph(node_id: str, depth: int, include_subblocks: bool = True) -> SubGraphDTO`
- **Method**: `validate_dag_cycle(new_edge: Edge) -> bool`
- **REST Endpoints**: `GET /api/v1/graph/nodes`, `GET /api/v1/graph/edges`
- **LLM Agent Tool**: `knowledge_search`

## 🚨 Strict Implementation & Quality Rules
- **Status Filter Enforcement**: Only nodes with `status: production` are included in active retrieval subgraphs (`NFR-SEC-01`).
- **Performance Benchmark (`NFR-PERF-02`)**: Incremental sync for 50,000 files must complete in **< 50ms**.
