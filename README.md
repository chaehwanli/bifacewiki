# Knowledge Platform (bifacewiki)

Dual-Layer Human Knowledge & AI Knowledge Management Ecosystem.

> **Full Documentation & User Manual**: [.doc/0816_user_manual_and_execution_guide.md](file:///home/chaehwan/bifacewiki/bifacewiki/.doc/0816_user_manual_and_execution_guide.md)  
> **Overall Architecture Spec**: [.doc/0816_knowledge_platform_architecture_spec.md](file:///home/chaehwan/bifacewiki/bifacewiki/.doc/0816_knowledge_platform_architecture_spec.md)  

---

## Quick Start & Execution Guide (실행 방법)

Knowledge Platform은 CLI 진입점(`src/cli.py`), HTTP REST API 웹 서버(`src/main.py`), 그리고 자동화 테스트 Suite (`tests/`)의 3가지 방식으로 즉시 실행 가능합니다.

### 1. CLI 터미널 실행 방법 (`src/cli.py`)

```bash
# 1-1. REST API 웹 서버 구동 (기본 포트: 8000)
python -m src.cli serve --port 8000

# 1-2. Q&A 대화 지식 추출 및 Draft 생성
python -m src.cli ingest --log "How to resolve memory leak in database connection pool?"

# 1-3. 인간 승인 대기 큐 목록 조회
python -m src.cli pending

# 1-4. 인간 중개자(Human Broker) 지식 승인 및 프로덕션 승격
python -m src.cli approve --node node-3d3b9bd8 --broker broker_alex

# 1-5. 프로덕션 지식 노드 검색
python -m src.cli search --query "memory leak"

# 1-6. 24/7 지식 자동 정적 린팅 (Broken link, Orphan node 등)
python -m src.cli audit

# 1-7. Ref-DAG 그래프 요약 조회
python -m src.cli graph
```

### 2. HTTP REST API 웹 서버 구동 (`src/main.py`)

```bash
# HTTP REST API 백엔드 서버 구동
python -m src.main 8000
```
- `POST /api/v1/knowledge/extract`: Q&A 추출 및 Draft 저장
- `GET /api/v1/approval/pending`: 승인 대기 목록 조회
- `POST /api/v1/approval/decide`: 인간 승인 결정 (`NFR-SEC-01` 통제)
- `POST /api/v1/audit/lint`: 24/7 정적 린팅 검사
- `GET /api/v1/graph/nodes` / `GET /api/v1/graph/edges`: 그래프 인덱스 조회
- `GET /api/v1/external/launch`: Obsidian/Logseq OS URI Scheme 연동

### 3. 자동화 테스트 Suite 실행 (`tests/`)

```bash
# 전체 단위/통합 테스트 (10개 Test Cases)
python -m pytest tests/ -v

# NFR 성능 벤치마크 지표 검증
python -m pytest tests/test_performance_benchmarks.py -v

# Kahn's Algorithm 기반 DAG 순환 방지 검증
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
