# Dashboard Menu Enhancements Implementation Plan (대시보드 보완 구현 계획서)

> **Document ID**: `0816_dashboard_enhancement_plan`  
> **Date**: 2026-08-16  
> **Author**: Antigravity AI & Knowledge Architecture Team  
> **Target Files**:  
> - `src/ui/index.html` (Main Presentation Layer Web UI)  
> - `src/main.py` (REST API Web Server Entry Point)  
> - `src/storage/git_operations_adapter.py` (Git Log & Diff Provider)  
> **Reference Document**: [.plan/0816_dashboard_usecase_evaluation.md](file:///home/chaehwan/bifacewiki/bifacewiki/.plan/0816_dashboard_usecase_evaluation.md)  

---

## 1. 개요 (Overview)

본 계획서는 [.plan/0816_dashboard_usecase_evaluation.md](file:///home/chaehwan/bifacewiki/bifacewiki/.plan/0816_dashboard_usecase_evaluation.md) 평가서에서 도출된 **부분 만족(4개)** 및 **미흡/개선 항목(2개)**을 완전한 만족상태(100% Satisfaction)로 승격시키기 위한 구체적 구현 상세 및 기술 로드맵을 정의합니다.

---

## 2. 세부 구현 대상 항목 (6 Target Areas)

| 번호 | 목표 유스케이스 | 영역 및 기능 | 관련 모듈 / API |
| :---: | :--- | :--- | :--- |
| **1** | `UC-004` & `UC-003` | **Git Management GUI 탭 신설**: Branch status, Commit timeline, Visual diff viewer, manual Push/Pull/Rollback controls | `src/ui/index.html`, `src/storage/git_operations_adapter.py`, `/api/v1/git/*` |
| **2** | `UC-005` | **Vendor-Agnostic LLM Selector UI 헤더 배치**: OpenAI, Gemini, Claude, Ollama 선택 드롭다운 및 Endpoint/API key 설정 | `src/ui/index.html`, `UniversalLLMVendorAdapter`, `/api/v1/settings/llm-vendor` |
| **3** | `UC-002` | **Ref-DAG Edge Matrix 시각화 탭 연동**: 노드 간 의존성/참조 관계 엣지 테이블 및 그래프 노드 관계 표현 | `src/ui/index.html`, `RefDAGIndexerEngine`, `/api/v1/graph/edges` |
| **4** | `UC-007` | **Knowledge Search & Context Inject Playground UI**: 사용자 질의 테스트 검색창, 검색 노드 결과 및 LLM Injected Context 미리보기 | `src/ui/index.html`, `KnowledgeRetrievalSkill`, `/api/v1/knowledge/search` |
| **5** | `UC-010` | **Graph Refactoring & Pruning Lifecycle Execution UI**: 유사도 >= 0.90 파편 노드 통합 제안/실행 및 Deprecated 노드 Archive 이관 액션 | `src/ui/index.html`, `GraphRefactoringEngine`, `/api/v1/refactor/*` |

---

## 3. 세부 모듈별 변경 사항 (Detailed Module Changes)

### 3.1 REST API Backend (`src/main.py` & `src/storage/git_operations_adapter.py`)
1. `GitOperationsAdapter`:
   - `get_commit_history(limit: int = 10) -> List[CommitDTO]` 메쏘드 추가.
2. `src/main.py`:
   - `GET /api/v1/git/history`: 커밋 이력 타임라인 리스트 반환.
   - `GET /api/v1/git/diff`: 커밋간 또는 HEAD 라인별 Diff 반환.
   - `POST /api/v1/git/sync`: Remote Push/Pull 동기화 실행.
   - `POST /api/v1/git/rollback`: 커밋 Revert 롤백 실행.
   - `GET/PUT /api/v1/settings/llm-vendor`: 활성 LLM 공급자 조회 및 원클릭 변경.
   - `POST /api/v1/knowledge/search`: 사용자 질의 기반 지식 탐색 및 조립된 Context String 반환.
   - `GET/POST /api/v1/refactor/candidates`, `/api/v1/refactor/merge`, `/api/v1/refactor/prune`: 중복 노드 통합 플랜 생성/실행 및 낡은 노드 아카이빙.

### 3.2 Web Frontend UI (`src/ui/index.html`)
1. **Header LLM Vendor Controls (`UC-005`)**:
   - 상단 헤더 오른쪽에 Active LLM Selector 드롭다운 (`OpenAI GPT-4o`, `Google Gemini 1.5 Pro`, `Anthropic Claude 3.5`, `Local Ollama`) 추가.
2. **Git Management Tab (`UC-004`, `UC-003`)**:
   - `⚙️ Git 저장소 & Diff 관리` 신규 탭 추가 (`tab-git`).
   - Branch Status 카드, Commit History 타임라인 리스트, Visual Line-by-Line Diff Modal 뷰어, `[Sync Remote]`, `[Rollback]` 버튼 렌더링.
3. **Graph & Edge Matrix Tab (`UC-002`, `UC-011`)**:
   - Existing Tab 5 (`tab-graph`) 확장: Active Nodes 리스트 외에 `Edges Matrix` (Source -> Target 참조 및 의존성 관계) 테이블 추가.
4. **Knowledge Search Playground Widget (`UC-007`)**:
   - Tab 3 (`tab-agent`) 또는 전용 영역에 지식 검색 키워드 입력창 및 `[Knowledge Context Inject Test]` 버튼 추가. 조립된 마크다운 렌더링.
5. **Graph Refactoring & Lifecycle Control Widget (`UC-010`)**:
   - Tab 4 (`tab-audit`) / Tab 5에 파편화 노드 통합 제안 카드(`[Execute Merge Plan]`) 및 180일 경과 Stale 노드 Archive 정리 버튼(`[Archive Stale Nodes]`) 추가.

---

## 4. 검증 계획 (Verification Plan)

1. **자동/REST API 검증**:
   - `curl` 또는 Python 테스트 스크립트로 새로 추가된 REST API 엔드포인트 (`GET /api/v1/git/history`, `PUT /api/v1/settings/llm-vendor`, `POST /api/v1/knowledge/search`, `POST /api/v1/refactor/merge`) 검증.
2. **웹 UI 기능 검증**:
   - `python -m src.main 8000` 웹 서버에서 대시보드 탭 전환 및 모든 신규 UI 기능 (Git Diff 조회, LLM 벤더 변경, 검색 테스트, 노드 통합, Obsidian URI 호출) 스크린샷/동작 확인.
