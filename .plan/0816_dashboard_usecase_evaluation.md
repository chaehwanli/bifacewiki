# Dashboard Menu vs Use Case Satisfaction Evaluation Report (대시보드 메뉴별 유스케이스 충족도 평가서)

> **Document ID**: `0816_dashboard_usecase_evaluation`  
> **Date**: 2026-08-16  
> **Author**: Antigravity AI & Knowledge Architecture Team  
> **Target Application**: Bifacewiki Knowledge Platform Web UI (`src/ui/index.html`, `src/ui/git_management_dashboard.tsx`, `src/main.py`)  
> **Reference Document**: [.doc/0816_usecase_spec.md](file:///home/chaehwan/bifacewiki/bifacewiki/.doc/0816_usecase_spec.md)  

---

## 1. 개요 (Overview)

본 평가서에서는 **Bifacewiki Knowledge Platform**의 대시보드 메뉴 구성(`src/ui/index.html` 및 `src/ui/git_management_dashboard.tsx`)이 표준 유스케이스 명세서([.doc/0816_usecase_spec.md](file:///home/chaehwan/bifacewiki/bifacewiki/.doc/0816_usecase_spec.md))에 정의된 **11가지 핵심 유스케이스(UC-001 ~ UC-011)**를 얼마나 충족(Satisfaction)하고 있는지 세부 매핑하고, 보완이 필요한 개선 항목을 도출합니다.

---

## 2. 대시보드 메뉴-유스케이스 매핑 및 평가 종합 (Evaluation Summary)

### 2.1 종합 평가 현황 (Summary Dashboard)

| 구분 | 유스케이스 수 | 비율 | 해당 유스케이스 ID |
| :--- | :---: | :---: | :--- |
| **✅ 완전 만족 (Satisfied)** | **5개** | 45.5% | UC-001, UC-006, UC-008, UC-009, UC-011 |
| **🟡 부분 만족 (Partially Satisfied)** | **4개** | 36.4% | UC-002, UC-003, UC-007, UC-010 |
| **⚠️ 미흡/개선 필요 (Needs Improvement)** | **2개** | 18.2% | UC-004, UC-005 |
| **합계** | **11개** | **100%** | **UC-001 ~ UC-011** |

---

### 2.2 유스케이스별 세부 충족도 검증 (Detailed Evaluation)

#### UC-001: Q&A 지식 추출 및 저장 (Q&A Ingestion & Extraction)
- **대시보드 메뉴**: 탭 1 `📥 Q&A 지식 추출` (`tab-ingest`)
- **구현 기능**: Q&A 대화 텍스트 입력 UI, `POST /api/v1/knowledge/extract` API 호출, 원자적(Atomic) 마크다운 자동 요약 및 `.drafts/` 격리 저장 결과 카드 출력.
- **충족 여부**: **✅ 완전 만족 (Satisfied)**
- **평가 소견**: 사용자가 Q&A 대화를 대시보드 입력창에 넣고 실행하면 원자적 노드 생성 및 `status: draft` 격리 저장이 완벽히 수행됨.

---

#### UC-002: Node & Edge 체계적 분류 (Node & Edge Structure & Parsing)
- **대시보드 메뉴**: 탭 5 `🕸️ Ref-DAG 그래프 탐색` (`tab-graph`)
- **구현 기능**: 활성 지식 노드 목록 조회 (`GET /api/v1/graph/nodes`) 및 상태 뱃지 렌더링.
- **충족 여부**: **🟡 부분 만족 (Partially Satisfied)**
- **평가 소견**: 노드 목록은 정상 노출되나, 노드 간 의존성 관계인 Edge Matrix (`GET /api/v1/graph/edges`)를 대시보드 상에서 직접 시각화하는 UI가 미비함 (Obsidian 외부 연동에 전담중).

---

#### UC-003: Git Repository 저장 및 관리 편의성 (Git Persistence & Operations)
- **대시보드 메뉴**: 승인/추출 처리 시 백엔드 연동 (`src/storage/git_operations_adapter.py`)
- **구현 기능**: 승인 관문(`approve`) 및 린팅 후 Git 자동 커밋 지원.
- **충족 여부**: **🟡 부분 만족 (Partially Satisfied)**
- **평가 소견**: 백엔드 자동 커밋 트랜잭션은 완전하게 동작하나, 사용자가 대시보드 상에서 수동으로 Git Push / Sync 상태를 직접 트리거하는 독자 메뉴는 탭 4/5에 통합되어 있지 않음.

---

#### UC-004: Git 생성 및 관리를 위한 UI 제공 (Git Management GUI & Dashboard)
- **대시보드 메뉴**: `src/ui/git_management_dashboard.tsx` (독립 React 컴포넌트)
- **구현 기능**: Git Branch 상태, Unstaged Count, Commit Timeline, Visual Line-by-Line Diff Viewer.
- **충족 여부**: **⚠️ 미흡/개선 필요 (Needs Improvement)**
- **평가 소견**: React 기반 대시보드 컴포넌트(`git_management_dashboard.tsx`)는 구현되어 있으나, 현재 메인 웹 서버 실행점인 `src/ui/index.html`에 전용 "Git 관리 대시보드" 탭으로 통합 렌더링되지 않아 접속 경로가 분리되어 있음.

---

#### UC-005: Vendor-Agnostic 지식 유지 (Vendor-Agnostic Knowledge Access Layer)
- **대시보드 메뉴**: 미배치 (UI 선택 폼 누락)
- **구현 기능**: 백엔드 Universal LLM Adapter (`UniversalLLMVendorAdapter`) 구현 완료.
- **충족 여부**: **⚠️ 미흡/개선 필요 (Needs Improvement)**
- **평가 소견**: 백엔드는 OpenAI, Gemini, Local Ollama 간 벤더 어댑팅을 지원하나, 대시보드 상단/설정 메뉴에 활성 LLM 공급자를 원클릭 변경하는 UI 선택 드롭다운이 누락되어 있음.

---

#### UC-006: Skill & Prompt 원클릭 주입 UI 제공 (One-Click Skill & Prompt Binding UI)
- **대시보드 메뉴**: 탭 3 `🤖 Agent 스킬 바인딩` (`tab-agent`)
- **구현 기능**: `qa_ingestion`, `knowledge_retrieval`, `linter_audit`, `refactor_merge` 4대 프리셋 카드 및 `POST /api/v1/agent/bind-skill` 원클릭 바인딩 버튼.
- **충족 여부**: **✅ 완전 만족 (Satisfied)**
- **평가 소견**: 복사-붙여넣기 없이 UI 버튼 한 번으로 `.agent/` 프롬프트를 런타임 세션에 즉시 바인딩하여 REQ-AGENT-BIND-01 요구사항을 충족함.

---

#### UC-007: Agent/Skill을 통한 LLM 지식 제공 (Agent & Skill Retrieval & Injection)
- **대시보드 메뉴**: 탭 3 (Retrieval Skill Binding) 및 백엔드 Retrieval API (`/api/v1/graph/nodes`)
- **구현 기능**: Agent Tool Calling 및 Context Injection 백엔드 모듈 완비.
- **충족 여부**: **🟡 부분 만족 (Partially Satisfied)**
- **평가 소견**: LLM 세션 스킬 주입은 대시보드 탭 3에서 지원되나, 대시보드 내에 직접 사용자가 지식 탐색 질의를 테스트할 수 있는 "Knowledge Search & Context Inject Playground" UI 위젯이 추가되면 완벽함.

---

#### UC-008: 지식 정합성 검사 및 자동 린팅 (Knowledge Linting & Consistency Audit)
- **대시보드 메뉴**: 탭 4 `🔍 정적 린팅 스캔` (`tab-audit`)
- **구현 기능**: `POST /api/v1/audit/lint` 호출, 24/7 static linter scan 실행, Broken Wikilinks, Orphan Nodes, Stale Nodes 결과 카드 실시간 리포팅.
- **충족 여부**: **✅ 완전 만족 (Satisfied)**
- **평가 소견**: 버튼 원클릭으로 지식 저장소 내 참조 깨짐 및 고립 노드를 실시간 정적 진단하고 요약 리포트를 가시화함.

---

#### UC-009: 인간 검증 및 승인 관문 (Human Approval & Knowledge Brokerage Gate)
- **대시보드 메뉴**: 탭 2 `🛡️ 인간 승인 관문` (`tab-approval`)
- **구현 기능**: `GET /api/v1/approval/pending` 대기 큐 조회, `author_type: ai_generated` 배지 가시화, Extracted Markdown 미리보기, `[Approve & Merge]`, `[Reject]` 결정 트랜잭션.
- **충족 여부**: **✅ 완전 만족 (Satisfied)**
- **평가 소견**: `NFR-SEC-01` 통제 정책에 따라 AI 지식의 프로덕션 무단 직접 반영을 차단하고 인간 중개자 승인 절차를 대시보드 관문으로 완벽 제공함.

---

#### UC-010: 지식 병합 및 폐기 수명주기 관리 (Knowledge Refactoring & Pruning Lifecycle)
- **대시보드 메뉴**: 탭 3 프리셋 카드 (`refactor_merge_preset`) 및 백엔드 `GraphRefactoringEngine`
- **구현 기능**: 파편화 노드 중복 통합 제안 스킬 바인딩.
- **충족 여부**: **🟡 부분 만족 (Partially Satisfied)**
- **평가 소견**: 스킬 주입 탭 3에는 리팩토링 스킬이 존재하나, 대시보드 탭 4(린팅)나 탭 5(그래프) 내에서 유사도 0.90 이상 중복 노드 통합(Merge) 및 Stale 노드 Archive 폐기를 즉시 실행하는 액션 버튼/트리거 UI가 보완될 필요가 있음.

---

#### UC-011: 외부 그래프 뷰어 툴 연동 및 등록 (External Graph Viewer Tool Integration)
- **대시보드 메뉴**: 탭 5 `🕸️ Ref-DAG 그래프 탐색` (`tab-graph`)
- **구현 기능**: 노드별 `[Obsidian으로 직접 열기]` 버튼, `GET /api/v1/external/launch` API 호출, OS 레벨 URI Scheme (`obsidian://open?file=...`) 자동 발송.
- **충족 여부**: **✅ 완전 만족 (Satisfied)**
- **평가 소견**: 별도 그래프 시각화 엔진 개발 없이 Obsidian 전문 PKM 툴과의 원클릭 연동을 완벽 제공하여 `NFR-COMP-01` 제로-코딩 연동을 달성함.

---

## 3. 대시보드 메뉴 권장 개선 로드맵 (Actionable Improvement Plan)

대시보드가 11가지 유스케이스를 **100% 완전 만족**하도록 하기 위해 다음 3가지 UI 통합 작업을 제안합니다.

1. **UC-004 Git 관리 탭 추가**:
   - `src/ui/index.html` 탭 네비게이션에 `⚙️ Git 저장소 & Diff 관리` 탭 신설.
   - `git_management_dashboard.tsx`에서 정의된 Git Status, Commit Timeline, Visual Line-by-Line Diff Viewer UI를 메인 HTML 탭으로 통합.

2. **UC-005 LLM Vendor Selector UI 상단 헤더 배치**:
   - 헤더 영역에 `[LLM Vendor: OpenAI / Gemini / Ollama Local]` 드롭다운 추가.
   - 벤더 선택 시 `PUT /api/v1/settings/llm-vendor` 백엔드 호환 연동.

3. **UC-002/UC-010 Edge 관계 및 그래프 리팩토링 액션 UI 추가**:
   - 탭 5 그래프 탐색 탭에 Edge 의존성 관계 테이블 및 `[유사 노드 통합 리팩토링 실행]` 버튼 추가.

---

## 4. 결론 (Conclusion)

현재 Bifacewiki Knowledge Platform의 대시보드는 핵심 흐름인 **지식 추출(UC-001)**, **스킬 바인딩(UC-006)**, **정적 린팅(UC-008)**, **인간 승인 관문(UC-009)**, **Obsidian 연동(UC-011)**의 5개 핵심 유스케이스를 완벽히 만족하고 있으며, 나머지 유스케이스도 백엔드 엔진 차원에서 이미 지원되고 있습니다. 

위 3가지 UI 개선 항목을 추가 반영하면 대시보드 메뉴만으로 11개 모든 유스케이스를 100% 커버하는 완벽한 Presentation Layer가 완성됩니다.
