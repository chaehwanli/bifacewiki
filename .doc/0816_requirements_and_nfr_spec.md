# Knowledge Platform Requirements & NFR Specification (요구사항 및 비기능 명세서)

> **Document ID**: `0816_requirements_and_nfr_spec`  
> **Date**: 2026-08-16  
> **Author**: Antigravity AI & Knowledge Architecture Team  
> **Related Architecture Document**: [.doc/0816_knowledge_platform_architecture_spec.md](file:///home/chaehwan/bifacewiki/bifacewiki/.doc/0816_knowledge_platform_architecture_spec.md)  
> **Related Use Case Document**: [.doc/0816_usecase_spec.md](file:///home/chaehwan/bifacewiki/bifacewiki/.doc/0816_usecase_spec.md)  
> **Status**: Approved Requirements Standard (Final Specification)  

---

## 1. 개요 (Overview)

본 문서는 Knowledge Platform의 유스케이스(UC-001 ~ UC-011)와 시스템 아키텍처에 정의된 기능 및 비기능 요구사항을 체계적으로 정의하고, 요구사항(REQ), 설계 모듈(DSGN), 검증 테스트(TEST), 그리고 비기능 요구사항(NFR) 간의 추적성(Traceability)을 구체적인 명세로 정리한 전용 요구사항 표준 레퍼런스 문서입니다.

---

## 2. 기능 요구사항 명세서 (Functional Requirements Specification: REQ)

| 요구사항 ID | 요구사항명 (Title) | 상세 설명 (Description) | 연관 유스케이스 (Related UC) | 우선순위 (Priority) | 분류 (Category) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **REQ-INGEST-01** | Q&A 대화 기반 지식 추출 및 Atomic 문서 생성 | 사용자와 LLM 간의 대화 히스토리를 분석하여 핵심 문제 해결책을 1개의 원자적(Atomic) 주제를 가진 마크다운 지식 노드로 추출 및 정제함. | `UC-001` | High | Ingestion |
| **REQ-INGEST-02** | Negative Knowledge (실패/안티패턴) 지식화 | 실패한 접근법, 오류 유발 동작, 안티패턴을 은폐하지 않고 `type: negative_knowledge` 메타데이터 속성을 부여하여 독립된 지식 자산으로 수집함. | `UC-001` | High | Ingestion |
| **REQ-GRAPH-01** | Frontmatter 메타데이터 파싱 및 Node 정의 | 마크다운 파일 상단의 YAML Frontmatter(`id`, `title`, `type`, `status`)를 정적 파싱하여 지식 그래프의 Node 객체로 수록함. | `UC-002` | High | Structure |
| **REQ-GRAPH-02** | Wikilink 및 Ref-DAG 인덱스 구축 | 본문 내 `[[Wikilink]]` 문법 및 메타데이터를 파싱하여 방향성 비순환 그래프(Ref-DAG) 형태의 In-Memory 연관 인덱스를 구축함. | `UC-002` | High | Structure |
| **REQ-STORAGE-01** | File-based Git 저장소 버전 관리 | 별도 RDBMS 없이 마크다운 파일 디렉토리를 Git 저장소로 관리하며 모든 지식 생성/수정/삭제 건을 원자적 커밋으로 기록함. | `UC-003` | High | Storage |
| **REQ-STORAGE-02** | Commit Diff 조회 및 원클릭 Rollback | 커밋 간 파일별 Visual Line Diff 정보를 제공하고, 필요한 경우 특정 과거 커밋 시점으로 지식을 안전하게 롤백(Revert)함. | `UC-003` | Medium | Storage |
| **REQ-UI-GIT-01** | Git 저장소 생성 및 원격 Sync GUI | Git CLI 명령어 없이 웹 대시보드 버튼 클릭으로 저장소 생성(`init`/`clone`) 및 Push/Pull 원격 동기화를 수행함. | `UC-004` | High | Management |
| **REQ-UI-GIT-02** | 저장소 상태 대시보드 및 Visual Diff 제공 | 저장소 내 Staged/Unstaged 파일 현황, 동기화 진행 상태, 변경 이력 타임라인을 시각적 GUI 렌더링으로 제공함. | `UC-004` | Medium | Management |
| **REQ-PLATFORM-01** | Vendor-Agnostic LLM 추상 어댑터 연동 | OpenAI, Gemini, Claude, Local Ollama 등 다양한 LLM 벤더로 전환 시에도 마크다운 지식 저장소 포맷 및 접근 방식을 동일하게 유지함. | `UC-005` | High | Platform |
| **REQ-AGENT-BIND-01** | Agent Skill & Prompt 원클릭 주입 UI | 대화창 입력란을 더럽히지 않고 UI 대시보드의 프리셋 카드 클릭 한 번으로 `.agent/` 내 스킬 및 프롬프트를 LLM 세션에 주입함. | `UC-006` | High | Agent |
| **REQ-RETRIEVAL-01** | Agent Skill 기반 LLM 지식 제공 및 Context 주입 | 하드코딩된 RAG 대신 Agent 표준 Skill(`knowledge_search`, `knowledge_retrieve`, `knowledge_context_inject`)을 매개로 Ref-DAG 지식을 동적으로 획득하여 주입함. | `UC-007` | High | Retrieval |
| **REQ-GOV-LINT-01** | 24/7 지식 정합성 자동 린팅 및 Audit 발행 | 깨진 Wikilink, 고립 노드(Orphan Node), 스키마 누락, 지식 간 모순(Contradiction)을 자동 감지하고 Audit 리포트를 생성함. | `UC-008` | High | Governance |
| **REQ-GOV-APPROVE-01** | Human Knowledge Broker 승인 관문 구축 | AI 생성 지식(`author_type: ai_generated`)을 바로 메인 저장소에 반영하지 않고 `draft` 상태로 대기시킨 후 인간 관리자가 검토/승인하는 관문을 제공함. | `UC-009` | High | Approval |
| **REQ-LIFECYCLE-01** | 지식 노드 통합(Merge) 및 폐기(Archive) 수명주기 | 유사도 높은 중복 파편화 노드를 1개 원자적 노드로 병합하고, 오래되었거나 오답인 노드를 `deprecated` 처리 후 Archive 영역으로 이관함. | `UC-010` | Medium | Lifecycle |
| **REQ-INTEG-OBS-01** | 외부 지식 툴(Obsidian/Logseq) 원클릭 연동 | 자체 3D 그래프 개발 대신 OS URI Scheme(`obsidian://open`)을 호출하여 등록된 외부 시각화 툴에서 지식 그래프 탐색을 수행함. | `UC-011` | Low | Exploration |

---

## 3. 설계 모듈 명세서 (Design Components Specification: DSGN)

명세서 2장 Module View에 정의된 각 설계 모듈의 식별자, 역할 및 연관 유스케이스 매핑입니다.

| 모듈 ID | 모듈명 (Title) | 상세 역할 및 책임 (Description) | 연관 유스케이스 (Related UC) | 소속 계층 (Layer) |
| :--- | :--- | :--- | :--- | :--- |
| **DSGN-CORE-INGEST** | `KnowledgeIngestionEngine` | Q&A 대화 세션을 파싱하여 3대 단순 규칙 준수 마크다운 문서 및 Minimal Frontmatter를 생성하는 정제 엔진. | `UC-001` | Core Engine |
| **DSGN-INDEXER-DAG** | `RefDAGIndexerEngine` | YAML Frontmatter 및 `[[Wikilinks]]`를 추출하여 In-Memory Ref-DAG 지식 그래프 인덱스 구조체를 유지/갱신하는 파서 엔진. | `UC-002` | Data & Storage |
| **DSGN-GIT-ADAPTER** | `GitOperationsAdapter` | 파일 시스템 기반 로컬/원격 Git 명령어(`add`, `commit`, `push`, `pull`, `diff`, `revert`)를 통제하는 백엔드 저장소 어댑터. | `UC-003` | Data & Storage |
| **DSGN-UI-DASHBOARD** | `GitManagementDashboard` | Git 저장소 현황, 동기화 진행바, 커밋 이력 타임라인 및 Line Diff 시각화를 담당하는 웹 프론트엔드 UI 모듈. | `UC-004` | Presentation |
| **DSGN-LLM-ADAPTER** | `UniversalLLMVendorAdapter` | OpenAI GPT, Google Gemini, Anthropic Claude, Local Ollama 등의 벤더 API 규격 차이를 일원화하여 어댑팅하는 인터페이스 모듈. | `UC-005` | Agent & Skill |
| **DSGN-AGENT-BINDER** | `SkillBindingMiddleware` | `.agent/skills/` 및 `prompts/` 내 템플릿을 읽어 LLM 런타임 세션의 System Prompt 및 Function Calling Schema에 주입하는 바인더. | `UC-006` | Agent & Skill |
| **DSGN-AGENT-SKILL** | `KnowledgeRetrievalSkill` | LLM의 Tool Calling 요청을 받아 Ref-DAG 인덱스 탐색 및 최적 지식 Context 묶음을 구성하여 반환하는 Agent 스킬 모듈. | `UC-007` | Agent & Skill |
| **DSGN-LINTER-ENGINE** | `KnowledgeLinterEngine` | 깨진 링크, Orphan Node, 스키마 오차, Contradiction을 정적 스캔하여 `lint_report.json` 및 Audit 대시보드 카드를 발행하는 린팅 엔진. | `UC-008` | Core Engine |
| **DSGN-APPROVAL-GATE** | `HumanApprovalGateManager` | Draft 상태 문서의 승인/반려/수정요청 워크플로우를 처리하고, 승인 시 `status: production` 변경 및 Git `main` 병합 커밋을 수행하는 관문 엔진. | `UC-009` | Core Engine |
| **DSGN-REFACTOR-ENGINE**| `GraphRefactoringEngine` | 유사 노드 자동 통합(Merge), Wikilink 리다이렉트 갱신, Stale Node 폐기(Archive) 수명주기 처리를 담당하는 그래프 리팩토링 엔진. | `UC-010` | Core Engine |
| **DSGN-LAUNCHER-PROTOCOL**| `ExternalLauncherAdapter` | OS 프로토콜 핸들러(`obsidian://open`)를 호출하여 지정된 저장소 디렉토리를 외부 전문 시각화 툴에서 자동 로딩시키는 연동 모듈. | `UC-011` | External Integration |

---

## 4. 검증 테스트 케이스 명세서 (Test Case Specification: TEST)

| 테스트 ID | 테스트 케이스명 (Title) | 검증 목적 및 테스트 절차 (Description) | 연관 유스케이스 (Related UC) | 연관 요구사항 | 테스트 유형 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TEST-UC001-01** | Q&A 지식 추출 및 Atomic 문서 생성 검증 | Q&A 대화 입력 시 1개 원자적 마크다운 지식 노드가 생성되고 Minimal Frontmatter(`type`, `title`) 및 `status: draft` 메타가 정상 결합되는지 검증함. | `UC-001` | `REQ-INGEST-01` | 통합 테스트 |
| **TEST-UC001-02** | Negative Knowledge 추출 및 분류 검증 | 실패 경험이나 안티패턴이 포함된 대화에서 `type: negative_knowledge` 속성이 정상 부여되고 주의사항 절이 생성되는지 검증함. | `UC-001` | `REQ-INGEST-02` | 기능 테스트 |
| **TEST-UC002-01** | Frontmatter 및 Wikilink Ref-DAG 파싱 검증 | 마크다운 내 Frontmatter 및 `[[Wikilink]]` 문법을 스캔하여 In-Memory Ref-DAG 인덱스가 오류 없이 구성되는지 검증함. | `UC-002` | `REQ-GRAPH-01`, `REQ-GRAPH-02` | 단위 테스트 |
| **TEST-UC003-01** | Git Commit, Diff 및 Rollback 검증 | 지식 문서 변경 시 원자적 Git 커밋이 생성되고, 커밋 간 Diff 조회 및 이전 커밋 시점으로의 Rollback(Revert)이 성공하는지 검증함. | `UC-003` | `REQ-STORAGE-01`, `REQ-STORAGE-02` | 통합 테스트 |
| **TEST-UC004-01** | Git GUI 저장소 생성 및 원격 Sync 검증 | 웹 대시보드 상에서 Git `init`/`clone` 및 Push/Pull 원격 동기화 클릭 시 상태바 및 Visual Diff가 정상 출력되는지 검증함. | `UC-004` | `REQ-UI-GIT-01`, `REQ-UI-GIT-02` | UI/E2E 테스트 |
| **TEST-UC005-01** | LLM Vendor 스위칭 지식 유지 검증 | UI에서 활성 LLM 공급자를 OpenAI에서 Gemini/Ollama로 전환한 후에도 지식 저장소 변경 없이 동일하게 작동하는지 검증함. | `UC-005` | `REQ-PLATFORM-01` | E2E 테스트 |
| **TEST-UC006-01** | 원클릭 Skill & Prompt 런타임 바인딩 검증 | UI 프리셋 카드 클릭 시 `.agent/skills/SKILL.md`가 읽혀 해당 LLM 대화 세션의 System Prompt 및 Tool Schema로 바인딩되는지 검증함. | `UC-006` | `REQ-AGENT-BIND-01` | 통합 테스트 |
| **TEST-UC007-01** | LLM Tool Calling 기반 지식 탐색/주입 검증 | LLM이 `knowledge_search()` Tool Call 발행 시 Ref-DAG 인덱스 탐색 후 정확한 마크다운 지식 Context가 답변에 주입되는지 검증함. | `UC-007` | `REQ-RETRIEVAL-01` | E2E 테스트 |
| **TEST-UC008-01** | Broken Link 및 Orphan Node 자동 린팅 검증 | 존재하지 않는 노드 참조나 고립 문서 포함 시 Linter가 이를 스캔하여 Audit 대시보드 리포트에 정확히 감지해 노출하는지 검증함. | `UC-008` | `REQ-GOV-LINT-01` | 단위/통합 테스트 |
| **TEST-UC009-01** | Human Approval Gate 승인 및 Main 병합 검증 | Draft 상태 지식에 대해 인간 관리자가 [Approve] 클릭 시 `status: production`으로 전환되고 Git `main` 브랜치에 병합 커밋되는지 검증함. | `UC-009` | `REQ-GOV-APPROVE-01` | E2E 테스트 |
| **TEST-UC010-01** | 중복 노드 통합 및 Wikilink 리다이렉트 검증 | 유사 노드 2개 병합 요청 시 1개 원자적 노드로 통합되고 기존 구 링크들이 신규 노드 ID로 자동 리다이렉트 갱신되는지 검증함. | `UC-010` | `REQ-LIFECYCLE-01` | 통합 테스트 |
| **TEST-UC011-01** | 외부 그래프 뷰어 (Obsidian) 원클릭 연동 검증 | UI 상의 [Open Graph in Obsidian] 버튼 클릭 시 OS URI Scheme(`obsidian://open`)이 정상 호출되어 외부 앱이 실행되는지 검증함. | `UC-011` | `REQ-INTEG-OBS-01` | UI/OS 테스트 |

---

## 5. 비기능 요구사항 명세서 (Non-Functional Requirements Specification: NFR)

플랫폼의 성능(Performance), 보안 및 권한(Security), 신뢰성 및 가용성(Reliability), 유지보수성 및 확장성(Maintainability), 호환성 및 사용성(Compatibility) 측면의 상세 지표와 규격입니다.

| NFR ID | 분류 (Category) | 항목명 (Title) | 구체적 지표 및 측정/검증 규격 (Metric & Criteria) | 연관 유스케이스 (Related UC) |
| :--- | :--- | :--- | :--- | :--- |
| **NFR-PERF-01** | Performance | 지식 추출 및 마크다운 정제 시간 | 사용자가 Q&A 대화 지식 추출을 요청한 시점부터 Atomic Markdown 및 Minimal Frontmatter가 생성되어 Draft로 완료되기까지의 시간 **< 3초** (네트워크 지연 제외). | `UC-001` |
| **NFR-PERF-02** | Performance | Ref-DAG 그래프 파싱 및 인덱싱 속도 | 1,000개 마크다운 문서 기준 전체 Frontmatter 파싱, Wikilink 추출 및 In-Memory Ref-DAG 인덱스 전수 업데이트 완료 시간 **< 1초**, 파서 메모리 점유율 **< 100MB**. | `UC-002` |
| **NFR-PERF-03** | Performance | Local Git 저장소 영속화 처리 속도 | 지식 파일 생성/수정 후 Local Git Commit 및 파일 변경 Diff 계산 완료 반응 시간 **< 500ms**. | `UC-003`, `UC-004` |
| **NFR-PERF-04** | Performance | One-Click Skill UI 바인딩 응답 속도 | UI 상에서 스킬 프리셋 카드 클릭 시 backend Skill 로딩 및 LLM 런타임 세션 System Prompt/Tool 바인딩 완료 처리 시간 **< 200ms**, UI 상태 반영 지연 **< 50ms**. | `UC-006` |
| **NFR-PERF-05** | Performance | Agent 지식 탐색 및 Context 주입 반응성 | LLM이 `knowledge_search` Tool Call 발행 시 Ref-DAG 연관 탐색 및 Context 반환 응답 지연 시간 **< 500ms**, 지식 전달 정확도 **90% 이상**. | `UC-007` |
| **NFR-SEC-01** | Security | AI 지식 승인 권한 격리 (Model Collapse 방지) | AI가 자동 생성한 지식(`author_type: ai_generated`)은 인간 중개자(Knowledge Broker)의 승인 없이 결코 `status: production` 및 Git `main` 브랜치로 자동 반영될 수 없음. | `UC-009` |
| **NFR-SEC-02** | Security | Git Remote Sync 인증 정보 보안 | 원격 Git 저장소(GitHub/GitLab) 연동 시 사용되는 SSH Private Key 및 Access Token은 OS Keychain 또는 암호화 저장소에 보관하며 통신 시 TLS 1.3 암호화를 의무화함. | `UC-003`, `UC-004` |
| **NFR-SEC-03** | Security | 로컬 LLM (Ollama) 사내 망 데이터 격리 | 로컬 LLM 모드 바인딩 시 지식 저장소 데이터 및 프롬프트가 외부 공용 인터넷 클라우드로 유출되지 않도록 완전한 사내/로컬 로컬호스트 통신만을 허용함. | `UC-005` |
| **NFR-RELI-01** | Reliability | 지식 데이터 무손실성 (Zero Data Loss) | 파일 시스템 무단 덮어쓰기를 금지하고 모든 지식 변경을 Git 커밋 이력으로 저장함으로써 무단 지식 유실 및 데이터 손실률 **0%**를 보장함. | `UC-003` |
| **NFR-RELI-02** | Reliability | 린터 정합성 검출 정확도 | 지식 저장소 내 존재하지 않는 깨진 참조(Broken Wikilinks) 및 고립 노드(Orphan Node) 탐지 정확도 **99% 이상** 준수. | `UC-008` |
| **NFR-RELI-03** | Reliability | Ref-DAG 순환 참조 방지 가용성 | 지식 간 의존성 연결 시 순환 참조(Circular Dependency)가 발생하지 않도록 인덱서 레벨에서 DAG 순환 검증을 의무화함. | `UC-002` |
| **NFR-MAINT-01** | Maintainability | LLM 공급자 제로 이관 비용 (Vendor Independence) | LLM 벤더(OpenAI, Gemini, Local) 변경 시 축적된 마크다운 지식 파일의 포맷 변환 및 재작성 작업 건수 **0건** (100% 호환 보장). | `UC-005` |
| **NFR-MAINT-02** | Maintainability | Atomic Knowledge 정량 규약 | 1개 마크다운 파일 당 단 1개의 주제만 다루도록 산출물 크기를 단일 원자 단위로 유지하여 지식 유지보수 및 리팩토링 복잡도를 대폭 줄임. | `UC-001`, `UC-002`, `UC-010` |
| **NFR-COMP-01** | Compatibility | 외부 PKM 툴 제로 코딩 연동 호환성 | 마크다운 표준, YAML Frontmatter 및 `[[Wikilinks]]` 마크업 표준을 100% 준수하여 별도 어댑터 개발 없이 Obsidian, Logseq 등의 외부 Vault로 즉시 연동됨. | `UC-011` |

---

## 6. 결언 및 문서 활용 가이드

본 명세서는 **REQ (기능 요구사항)**, **DSGN (설계 모듈)**, **TEST (검증 테스트 케이스)**, **NFR (비기능 요구사항)** 간의 완전한 매핑 체계를 제공합니다.

1. **명세서 동기화**: [.doc/0816_knowledge_platform_architecture_spec.md](file:///home/chaehwan/bifacewiki/bifacewiki/.doc/0816_knowledge_platform_architecture_spec.md) 및 [.doc/0816_usecase_spec.md](file:///home/chaehwan/bifacewiki/bifacewiki/.doc/0816_usecase_spec.md)의 UC-001 ~ UC-011 상세 명세서 내 추적성(Traceability) 및 비기능(NFR) 항목을 본 문서의 정식 식별 태그로 참조 동기화합니다.
2. **개발 및 검증 기준**: 개발팀은 `DSGN` 모듈 단위로 코드를 작성하고, QA팀은 `TEST` 케이스를 바탕으로 단위/통합 테스트를 진행하며, `NFR` 기준을 기준으로 시스템 성능 및 보안을 검증합니다.
