# Dashboard Enhancement TDD Implementation Task Plan (대시보드 보완 TDD 구현 태스크 계획서)

> **Document ID**: `0816_dashboard_tdd_task_plan`  
> **Date**: 2026-08-16  
> **Author**: Antigravity AI & Knowledge Architecture Team  
> **Skill References**:  
> - [.skill/presentation_ui/SKILL.md](file:///home/chaehwan/bifacewiki/bifacewiki/.skill/presentation_ui/SKILL.md)  
> - [.skill/git_adapter/SKILL.md](file:///home/chaehwan/bifacewiki/bifacewiki/.skill/git_adapter/SKILL.md)  
> **Target Files**:  
> - `src/storage/git_operations_adapter.py`  
> - `src/main.py`  
> - `src/ui/index.html`  
> - `tests/test_dashboard_enhancements.py` (New Test File)  

---

## 1. 개요 (Overview)

본 계획서는 [.plan/0816_dashboard_enhancement_plan.md](file:///home/chaehwan/bifacewiki/bifacewiki/.plan/0816_dashboard_enhancement_plan.md)를 바탕으로, TDD(Test-Driven Development: 테스트 구동 개발) 방법론을 적용하여 Knowledge Platform 대시보드의 미흡/부분 만족 유스케이스 6종을 5개 단계(Phase 1 ~ Phase 5)에 걸쳐 체계적으로 구현하기 위한 상세 태스크 목록 및 테스트 케이스를 정의합니다.

---

## 2. SKILL 보강 현황 (Skill Reinforcement Status)

구현 시작에 앞서 아래 2개 기능별 스킬 문서가 확장보강 완료되었습니다.

1. **[.skill/presentation_ui/SKILL.md](file:///home/chaehwan/bifacewiki/bifacewiki/.skill/presentation_ui/SKILL.md)**:
   - Git Management Dashboard(`UC-004`), LLM Vendor Switcher(`UC-005`), Ref-DAG Edge Matrix(`UC-002`), Search Playground(`UC-007`), Graph Refactoring Widget(`UC-010`)에 대한 UI 규약 및 REST API 계약 정보 전면 추가.
2. **[.skill/git_adapter/SKILL.md](file:///home/chaehwan/bifacewiki/bifacewiki/.skill/git_adapter/SKILL.md)**:
   - `get_history(limit: int)` 메쏘드 명세 및 `GET /api/v1/git/history`, `GET /api/v1/git/diff` API 엔드포인트 명세 추가.

---

## 3. 단계별 TDD 구현 태스크 로드맵 (5-Phase TDD Task Roadmap)

### 🧪 Phase 1: Git Operations & Management REST API (TDD - `UC-003`, `UC-004`)
- **목표**: Git 커밋 이력 조회, 라인별 Diff, Remote Push/Pull Sync 및 Rollback API 연동
- **1-1. Red (테스트 작성)**:
  - `tests/test_dashboard_enhancements.py::test_git_adapter_get_history()`
  - `tests/test_dashboard_enhancements.py::test_api_git_history_endpoint()`
  - `tests/test_dashboard_enhancements.py::test_api_git_diff_endpoint()`
  - `tests/test_dashboard_enhancements.py::test_api_git_sync_endpoint()`
  - `tests/test_dashboard_enhancements.py::test_api_git_rollback_endpoint()`
- **1-2. Green (기능 구현)**:
  - `src/storage/git_operations_adapter.py`: `get_history(limit: int = 10) -> List[CommitDTO]` 메쏘드 작성
  - `src/main.py`: `GET /api/v1/git/history`, `GET /api/v1/git/diff`, `POST /api/v1/git/sync`, `POST /api/v1/git/rollback` 엔드포인트 핸들러 작성
- **1-3. Refactor (리팩토링 & 검증)**: `pytest` 실행하여 Phase 1 통과 확인

---

### 🧪 Phase 2: LLM Vendor Selector REST API (TDD - `UC-005`)
- **목표**: OpenAI, Gemini, Claude, Local Ollama 벤더 설정 원클릭 조회/수정 API 구축
- **2-1. Red (테스트 작성)**:
  - `tests/test_dashboard_enhancements.py::test_api_get_llm_vendor_settings()`
  - `tests/test_dashboard_enhancements.py::test_api_put_llm_vendor_settings()`
  - `tests/test_dashboard_enhancements.py::test_ollama_sandbox_isolation_nfr_sec_03()`
- **2-2. Green (기능 구현)**:
  - `src/main.py`: `GET /api/v1/settings/llm-vendor` 및 `PUT /api/v1/settings/llm-vendor` 라우팅 작성, `UniversalLLMVendorAdapter.switch_vendor()` 호출
- **2-3. Refactor (리팩토링 & 검증)**: `pytest` 실행하여 벤더 전환 및 Ollama Localhost Sandbox (`NFR-SEC-03`) 작동 검증

---

### 🧪 Phase 3: Ref-DAG Edges Matrix & Refactoring Lifecycle API (TDD - `UC-002`, `UC-010`)
- **목표**: Edge 의존성 관계 조회, 중복 노드 통합 제안/실행 및 Stale 노드 아카이빙 API 구축
- **3-1. Red (테스트 작성)**:
  - `tests/test_dashboard_enhancements.py::test_api_graph_edges()`
  - `tests/test_dashboard_enhancements.py::test_api_refactor_candidates()`
  - `tests/test_dashboard_enhancements.py::test_api_refactor_merge_execution()`
  - `tests/test_dashboard_enhancements.py::test_api_refactor_prune_stale()`
- **3-2. Green (기능 구현)**:
  - `src/main.py`: `GET /api/v1/graph/edges`, `GET /api/v1/refactor/candidates`, `POST /api/v1/refactor/merge`, `POST /api/v1/refactor/prune` 작성 및 `GraphRefactoringEngine` 연동
- **3-3. Refactor (리팩토링 & 검증)**: `pytest` 실행하여 노드 통합 및 Wikilink 자동 리다이렉트 검증

---

### 🧪 Phase 4: Knowledge Search & Context Inject Playground API (TDD - `UC-007`)
- **목표**: 사용자 질의 기반 지식 탐색 및 조립된 Knowledge Context 반환 API 구축
- **4-1. Red (테스트 작성)**:
  - `tests/test_dashboard_enhancements.py::test_api_knowledge_search_and_context_injection()`
- **4-2. Green (기능 구현)**:
  - `src/main.py`: `POST /api/v1/knowledge/search` 구현, `KnowledgeRetrievalSkill.knowledge_search()` 및 `knowledge_context_inject()` 연동
- **4-3. Refactor (리팩토링 & 검증)**: `pytest` 검증

---

### 🎨 Phase 5: Web UI Presentation Integration (`src/ui/index.html`)
- **목표**: 구축된 REST API를 기반으로 `src/ui/index.html` 대시보드 렌더링 및 인터랙션 완비
- **5-1. UI 구현 항목**:
  1. Header 영역: `LLM Vendor Selector` 드롭다운 (`OpenAI`, `Gemini`, `Claude`, `Ollama`) 및 보안 뱃지 배치
  2. Tab 6 신설: `⚙️ Git 저장소 & Diff` (`tab-git`) - Branch Status, Commit Timeline, Visual Diff Modal, `[Sync Remote]`, `[Rollback]` 버튼
  3. Tab 5 확장: `Ref-DAG Graph & Edge Matrix` - Source -> Target 의존성 테이블 및 `[Obsidian으로 직접 열기]`
  4. Tab 3 확장: `Knowledge Search Playground` - 질의 테스트 입력창 및 조립된 Context 미리보기
  5. Tab 4 확장: `Graph Refactoring Widget` - 중복 노드 통합 카드(`[Execute Merge Plan]`) 및 Stale 노드 정리 버튼(`[Archive Stale Nodes]`)
- **5-2. UI 기능 동작 검증**: HTTP 서버 구동 후 탭 전환 및 모든 API 버튼 클릭 동작 확인

---

## 4. 진행 순서 및 승인 요청 (Execution Order)

1. **[완료] SKILL 보강**: `.skill/presentation_ui/SKILL.md`, `.skill/git_adapter/SKILL.md` 업데이트 완료
2. **[다음 단계] Phase 1 ~ Phase 4 TDD 개발 (Red -> Green -> Refactor)**: `tests/test_dashboard_enhancements.py` 작성 및 `src/storage/git_operations_adapter.py`, `src/main.py` 구현
3. **[최종 단계] Phase 5 Web UI 구현**: `src/ui/index.html` 통합 및 검증
