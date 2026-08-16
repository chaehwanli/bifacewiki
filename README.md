# Knowledge Platform (bifacewiki)

Dual-Layer Human Knowledge & AI Knowledge Management Ecosystem.

> **Full Documentation & User Manual**: [.doc/0816_user_manual_and_execution_guide.md](file:///home/chaehwan/bifacewiki/bifacewiki/.doc/0816_user_manual_and_execution_guide.md)  
> **Overall Architecture Spec**: [.doc/0816_knowledge_platform_architecture_spec.md](file:///home/chaehwan/bifacewiki/bifacewiki/.doc/0816_knowledge_platform_architecture_spec.md)  

---

## Quick Start (실행 방법)

### Automated Test Suite Execution
Run the full unit test suite, NFR benchmark latency test suite, and DAG cycle prevention tests:

```bash
# Run all unit and integration tests (10 test cases)
python -m pytest tests/ -v

# Run performance NFR benchmark latency tests
python -m pytest tests/test_performance_benchmarks.py -v

# Run Kahn's algorithm DAG cycle prevention tests
python -m pytest tests/test_dag_cycle_prevention.py -v
```

---

## 11 Core DSGN Modules Summary (제공하는 주요 기능)

1. **`DSGN-CORE-INGEST`** ([src/core/knowledge_ingestion_engine.py](file:///home/chaehwan/bifacewiki/bifacewiki/src/core/knowledge_ingestion_engine.py)): Q&A Log parsing, Atomic Markdown creation (`NFR-MAINT-02`), `.drafts/` isolation (`NFR-SEC-01`).
2. **`DSGN-INDEXER-DAG`** ([src/indexer/ref_dag_indexer_engine.py](file:///home/chaehwan/bifacewiki/bifacewiki/src/indexer/ref_dag_indexer_engine.py)): Ref-DAG 2-Tier Indexing (Memory + SQLite), Sub-block (`#heading`) parsing, 500ms Sliding Window File Watcher Debouncer, Kahn's algorithm cycle prevention (`NFR-RELI-03`).
3. **`DSGN-GIT-ADAPTER`** ([src/storage/git_operations_adapter.py](file:///home/chaehwan/bifacewiki/bifacewiki/src/storage/git_operations_adapter.py)): File-based Git commits, line-by-line visual diffs, rollback, OS Keychain remote sync (`NFR-SEC-02`).
4. **`DSGN-LINTER-ENGINE`** ([src/core/knowledge_linter_engine.py](file:///home/chaehwan/bifacewiki/bifacewiki/src/core/knowledge_linter_engine.py)): 24/7 static audit scanner detecting broken links, orphan nodes, YAML schema errors, 180d stale nodes, and contradictions.
5. **`DSGN-APPROVAL-GATE`** ([src/core/human_approval_gate_manager.py](file:///home/chaehwan/bifacewiki/bifacewiki/src/core/human_approval_gate_manager.py)): Human Broker review queue, promotion to `knowledge/` and `main` branch, strict AI self-approval block (`NFR-SEC-01`).
6. **`DSGN-REFACTOR-ENGINE`** ([src/core/graph_refactoring_engine.py](file:///home/chaehwan/bifacewiki/bifacewiki/src/core/graph_refactoring_engine.py)): Duplicate node consolidation ($\ge 0.90$ similarity), Wikilink auto-redirection, archiving deprecated nodes.
7. **`DSGN-LLM-ADAPTER`** ([src/agent/universal_llm_vendor_adapter.py](file:///home/chaehwan/bifacewiki/bifacewiki/src/agent/universal_llm_vendor_adapter.py)): Universal connector for OpenAI, Gemini, Claude, and Localhost Proxy Sandbox for Ollama (`NFR-SEC-03`).
8. **`DSGN-AGENT-BINDER`** ([src/agent/skill_binding_middleware.py](file:///home/chaehwan/bifacewiki/bifacewiki/src/agent/skill_binding_middleware.py)): Dynamic skill loader binding system prompts and tool schemas to LLM sessions (`NFR-PERF-04` < 200ms).
9. **`DSGN-AGENT-SKILL`** ([src/agent/knowledge_retrieval_skill.py](file:///home/chaehwan/bifacewiki/bifacewiki/src/agent/knowledge_retrieval_skill.py)): Tool handlers (`knowledge_search`, `knowledge_retrieve`, `knowledge_context_inject`) restricted to `status: production` nodes.
10. **`DSGN-UI-DASHBOARD`** ([src/ui/git_management_dashboard.tsx](file:///home/chaehwan/bifacewiki/bifacewiki/src/ui/git_management_dashboard.tsx)): React Web UI dashboard rendering status widgets, commit timelines, visual diffs, and approval review cards.
11. **`DSGN-LAUNCHER-PROTOCOL`** ([src/ui/external_launcher_adapter.py](file:///home/chaehwan/bifacewiki/bifacewiki/src/ui/external_launcher_adapter.py)): OS URI scheme launcher (`obsidian://open?vault=...&file=...`) for external PKM tools (`NFR-COMP-01`).
