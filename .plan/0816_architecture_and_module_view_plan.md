# Knowledge Platform Overall Architecture & Module View Plan (작성 및 역할별 검토 플랜)

> **Document ID**: `0816_architecture_and_module_view_plan`  
> **Date**: 2026-08-16  
> **Author**: Antigravity AI Pair Programmer & Role-based Engineering Team  
> **Target Doc**: `.doc/0816_knowledge_platform_architecture_spec.md`  

---

## 1. 개요 (Overview)

본 문서는 `0816_usecase_spec.md` (UC-001 ~ UC-011) 및 `0816_requirements_and_nfr_spec.md` (REQ/DSGN/TEST/NFR)를 바탕으로 **Knowledge Platform Overall Architecture (전체 아키텍처)** 및 **Knowledge Platform Module View (모듈 뷰)**를 정의하기 위한 주체별(Role-based) 분석 및 작성 로드맵입니다.

GEMINI.md에 명시된 4개 주체별 스킬(Architect, PO, Developer, QA)을 독립된 시각에서 순차 적용하여, 구상만 포함된 개요 수준의 문서(Outline-only)를 배제하고 구현 가능 수준(Coding-ready)의 확정 아키텍처 사양서를 작성합니다.

---

## 2. 역할별(Role-based) 분석 및 작성 보완 의견

### 2.1 System Architect (`architect`) 역할 시각
- **전체 아키텍처 모델링 (Dual-Layer Architecture)**:
  - **Physical Storage Layer**: File-based Git Repository (Markdown 문서, YAML Frontmatter, `[[Wikilinks]]`).
  - **Logical Ref-DAG Graph Layer**: In-Memory Ref-DAG (Reference Directed Acyclic Graph) 지식 그래프 인덱서.
- **Ref-DAG 순환 방지 알고리즘 (DAG Constraint)**:
  - 노드 간 의존성 검증 시 **Kahn's Algorithm (Topological Sort)** 또는 **DFS Back-Edge Detection** 알고리즘 적용.
  - 순환 참조(Circular Dependency) 감지 시 트랜잭션 차단 및 린터 이슈 큐 등록 (`NFR-RELI-03`).
- **동적 시퀀스 플로우 (Mermaid Sequence Diagrams)**:
  1. **Ingestion & Atomic Node Flow**: Q&A대화 파싱 → Minimal Frontmatter 결합 → Draft 노드 영속화.
  2. **Knowledge Linting & Audit Flow**: Cron/파일이벤트 → Linter 정적 검사 → Broken Link/Orphan/Contradiction Audit 발행.
  3. **Human Approval Gate Flow**: Draft 지식 검토 → 인간 중개자 승인 → Metadata 갱신 → Git `main` 병합 커밋.
  4. **Dynamic Agent Retrieval Flow**: LLM Tool Call `knowledge_search` → Ref-DAG 연관 탐색 → Context Assembler → LLM Prompt 주입.
- **In-Memory 인덱스 갱신 및 캐시 무효화 (Cache Invalidation)**:
  - 파일 시스템 이벤트(inotify) 및 Git post-commit / post-merge 훅 연동 사전 갱신 트래킹.
- **보안 및 격리 경계**:
  - `status: production` 지식 격리 필터링 (`NFR-SEC-01`).
  - 사내망 망분리 로컬 LLM (Ollama) Localhost Proxy 경계 정의 (`NFR-SEC-03`).

### 2.2 Project Owner (`po`) 역할 시각
- **지식 거버넌스 및 수명주기(Lifecycle) 정책**:
  - 지식 상태 전이: `draft` → `review_pending` → `production` → `deprecated` / `archived`.
  - **디렉토리 및 브랜치 분리 규약**:
    - Draft: `.drafts/` 디렉토리 / 작업 브랜치.
    - Production: `knowledge/` 메인 디렉토리 / `main` 브랜치.
    - Archive: `archive/` 디렉토리 / `main` 브랜치.
  - Model Collapse 방지 (`NFR-SEC-01`): `author_type: ai_generated` 지식은 인간 승인 API (`POST /api/v1/approval/decide`) 거쳐야만 `main` 병합 허용.
- **비기술자 사용자 경험(Non-Technical User Readiness)**:
  - Git Management GUI (`DSGN-UI-DASHBOARD`): 저장소 생성/동기화 시각화, 진행 상태바, Line-by-Line Visual Diff modal, 원클릭 Rollback.
  - Skill & Prompt Binding UI (`DSGN-AGENT-BINDER`): 원클릭 프리셋 카드로 복사-붙여넣기 없이 세션 바인딩.

### 2.3 Tech Lead & Core Developer (`developer`) 역할 시각
- **개발 즉시 착수 가능(Coding Readiness) 사양 상세화**:
  - 11개 설계 모듈(`DSGN-CORE-INGEST` ~ `DSGN-LAUNCHER-PROTOCOL`)의 클래스/인터페이스 정의.
  - REST API 엔드포인트 URL, HTTP 메서드, JSON Request/Response DTO Payload Schema 명시.
  - 모듈 간 내부 이벤트(Event Payloads) 및 메서드 파라미터 규격 명시.
- **파서 및 어댑터 구체 명세**:
  - Frontmatter YAML AST 파서 및 `[[Wikilinks]]` 정규식/AST 파서 규격.
  - `GitOperationsAdapter` 메소드 명세 (`commit`, `diff`, `revert`, `push`, `pull`, `status`).
  - `UniversalLLMVendorAdapter` 다형성 인터페이스 (OpenAI, Gemini, Claude, Ollama).

### 2.4 QA Lead (`qa`) 역할 시각
- **추적성 매트릭스 (Traceability Matrix) 완비**:
  - `REQ-xxx` ↔ `DSGN-xxx` ↔ `TEST-xxx` ↔ `NFR-xxx` 매핑을 아키텍처 문서 내 모듈 테이블에 명시.
- **계약 테스트 및 샌드박스 뷰어 검증**:
  - LLM Tool Calling (`knowledge_search`, `knowledge_retrieve`) 계약 테스트용 스텁/모킹 정의.
  - Draft 지식의 LLM 주입 차단 검증 스나이퍼 테스트.
- **NFR 성능 측정 엔드포인트 수록**:
  - Ingestion Latency (< 3s, `NFR-PERF-01`), Ref-DAG Reindex Latency (< 1s / 1000 docs, `NFR-PERF-02`), Local Git Commit (< 500ms, `NFR-PERF-03`), Skill Binding (< 200ms, `NFR-PERF-04`), Context Injection (< 500ms, `NFR-PERF-05`) 검증용 벤치마크 가이드.

---

## 3. 사양서 문서 구조 계획 (`.doc/0816_knowledge_platform_architecture_spec.md`)

1. **문서 헤더 및 레퍼런스 정보**
2. **1. 개요 및 전체 아키텍처 (Overall Architecture)**
   - 1.1 시스템 아키텍처 목표 및 핵심 설계 원칙 (Dual-Layer & Atomic Knowledge)
   - 1.2 전체 계층 구조 다이어그램 (Mermaid System Architecture Diagram)
   - 1.3 4대 영역별 전체 구조 (Presentation, Core Engine, Data & Storage, Agent & Integration)
   - 1.4 지식 수명주기 및 브랜치/디렉토리 거버넌스 (PO 시약)
   - 1.5 Ref-DAG 그래프 모델링 및 순환 방지 알고리즘 (Architect 시각)
   - 1.6 핵심 런타임 동적 시퀀스 플로우 (Mermaid Sequence Diagrams 4종)
3. **2. 모듈 뷰 (Module View & Component Specification)**
   - 2.1 전체 모듈 구성도 및 DSGN ID 추적성 매트릭스
   - 2.2 Presentation Layer 모듈 상세 사양 (`DSGN-UI-DASHBOARD`)
   - 2.3 Core Engine Layer 모듈 상세 사양 (`DSGN-CORE-INGEST`, `DSGN-LINTER-ENGINE`, `DSGN-APPROVAL-GATE`, `DSGN-REFACTOR-ENGINE`)
   - 2.4 Data & Storage Layer 모듈 상세 사양 (`DSGN-INDEXER-DAG`, `DSGN-GIT-ADAPTER`)
   - 2.5 Agent & Integration Layer 모듈 상세 사양 (`DSGN-LLM-ADAPTER`, `DSGN-AGENT-BINDER`, `DSGN-AGENT-SKILL`, `DSGN-LAUNCHER-PROTOCOL`)
4. **3. API 및 데이터 전송 객체 (REST API & DTO Specifications)**
   - 3.1 REST API 엔드포인트 전체 목록
   - 3.2 DTO Payload JSON Schemas (Ingestion, Approval, Git, Skill, Lint, Launch)
5. **4. NFR 및 보안 격리 구현 사양 (Non-Functional & Security Architecture)**
   - 4.1 AI 지식 승인 권한 격리 (`NFR-SEC-01`)
   - 4.2 Git SSH/Token 보안 및 Localhost Proxy (`NFR-SEC-02`, `NFR-SEC-03`)
   - 4.3 Performance Benchmark & Instrumentation Guide (`NFR-PERF-01~05`)
6. **5. 종합 추적성 매트릭스 (Traceability Matrix)**
