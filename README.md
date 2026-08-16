# Knowledge Platform (bifacewiki)

Dual-Layer Human Knowledge & AI Knowledge Management Ecosystem.

> **Full Documentation & User Manual**: [.doc/0816_user_manual_and_execution_guide.md](file:///home/chaehwan/bifacewiki/bifacewiki/.doc/0816_user_manual_and_execution_guide.md)  
> **Overall Architecture Spec**: [.doc/0816_knowledge_platform_architecture_spec.md](file:///home/chaehwan/bifacewiki/bifacewiki/.doc/0816_knowledge_platform_architecture_spec.md)  

---

## Quick Start & Execution Guide (실행 방법)

Knowledge Platform은 **Standalone Web GUI App (웹 브라우저 GUI)**, **CLI 터미널 도구 (`src/cli.py`)**, **HTTP REST API 백엔드 서버 (`src/main.py`)**, 그리고 **자동화 테스트 Suite (`tests/`)**로 즉시 구동할 수 있습니다.

### 1. Standalone Web GUI App 구동 (웹 브라우저 UI)

사용자를 위한 웹 GUI 인터페이스 및 에이전트 스킬 바인딩을 제공하는 Standalone Web App을 구동합니다:

```bash
# 1. 서버 구동
python -m src.main 8000
# 또는
python -m src.cli serve --port 8000

# 2. 웹 브라우저 접속
http://127.0.0.1:8000/
```
- **대시보드 기능**: Git 상태, 타임라인, Visual Line-by-Line Diff 모달
- **인간 승인 대기 큐**: Draft 지식 리뷰, Markdown 비교, [Approve & Merge] / [Reject] 버튼 (`NFR-SEC-01`)
- **Agent Skill & Prompt Binder**: Visual 카드 UI를 통한 One-Click Prompt Preset 바인딩 (`DSGN-AGENT-BINDER`)
- **Graph Explorer & Obsidian**: 지식 그래프 탐색 및 `obsidian://open` OS URI 연동 (`UC-011`)

### 2. CLI 터미널 실행 방법 (`src/cli.py`)

```bash
# 2-1. Q&A 대화 지식 추출 및 Draft 생성
python -m src.cli ingest --log "How to resolve memory leak in database connection pool?"

# 2-2. 인간 승인 대기 큐 목록 조회
python -m src.cli pending

# 2-3. 인간 중개자(Human Broker) 지식 승인 및 프로덕션 승격
python -m src.cli approve --node node-3d3b9bd8 --broker broker_alex

# 2-4. 프로덕션 지식 노드 검색
python -m src.cli search --query "memory leak"

# 2-5. 24/7 지식 자동 정적 린팅 (Broken link, Orphan node 등)
python -m src.cli audit

# 2-6. Ref-DAG 그래프 요약 조회
python -m src.cli graph
```

### 3. Agent & Prompt Presets (`.agent/`)

LLM 및 에이전트에 공급되는 Prompt Preset 규약은 `.agent/` 디렉토리에 위치합니다:

- **`.agent/agent.json`**: Agent Configuration & Registered Skills
- **`.agent/prompts/qa_ingestion_preset.json`**: Q&A 추출 및 Atomic Markdown 생성 프롬프트 프리셋
- **`.agent/prompts/knowledge_retrieval_preset.json`**: Ref-DAG 검색 및 Context 주입 프롬프트 프리셋
- **`.agent/prompts/linter_audit_preset.json`**: 24/7 정적 린팅 프롬프트 프리셋
- **`.agent/prompts/refactor_merge_preset.json`**: 그래프 중복 통합 프롬프트 프리셋

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
10. **`DSGN-UI-DASHBOARD`** ([src/ui/git_management_dashboard.tsx](file:///home/chaehwan/bifacewiki/bifacewiki/src/ui/git_management_dashboard.tsx), [src/ui/index.html](file:///home/chaehwan/bifacewiki/bifacewiki/src/ui/index.html)): React & Standalone HTML/JS Web GUI rendering status widgets, commit timelines, visual diffs, and approval review cards.
11. **`DSGN-LAUNCHER-PROTOCOL`** ([src/ui/external_launcher_adapter.py](file:///home/chaehwan/bifacewiki/bifacewiki/src/ui/external_launcher_adapter.py)): OS URI scheme launcher (`obsidian://open?vault=...&file=...`) for external PKM tools (`NFR-COMP-01`).
