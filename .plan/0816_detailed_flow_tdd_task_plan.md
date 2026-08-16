# Detailed Runtime Flow TDD Task Plan (세분화 런타임 플로우 TDD 구현 태스크 계획서)

> **Document ID**: `0816_detailed_flow_tdd_task_plan`  
> **Date**: 2026-08-16  
> **Author**: Antigravity AI & Knowledge Architecture Team  
> **Target Document**: [.plan/0816_detailed_chat_and_auth_flow_plan.md](file:///home/chaehwan/bifacewiki/bifacewiki/.plan/0816_detailed_chat_and_auth_flow_plan.md)  
> **Skill References**:  
> - [.skill/presentation_ui/SKILL.md](file:///home/chaehwan/bifacewiki/bifacewiki/.skill/presentation_ui/SKILL.md)  
> - [.skill/agent_binder/SKILL.md](file:///home/chaehwan/bifacewiki/bifacewiki/.skill/agent_binder/SKILL.md)  
> - [.skill/ingestion/SKILL.md](file:///home/chaehwan/bifacewiki/bifacewiki/.skill/ingestion/SKILL.md)  
> **Target Implementation Files**:  
> - `src/main.py`  
> - `src/agent/agent_skill_binder.py`  
> - `src/core/knowledge_ingestion_engine.py`  
> - `tests/test_detailed_runtime_flows.py` (New Test File)  

---

## 1. 개요 (Overview)

본 태스크 계획서는 [.plan/0816_detailed_chat_and_auth_flow_plan.md](file:///home/chaehwan/bifacewiki/bifacewiki/.plan/0816_detailed_chat_and_auth_flow_plan.md)에 기술된 4개 세분화 런타임 플로우(인증/연결, 대화 세션 관리, 토큰 스트리밍/Tool Call, 지식 생성 UX 프로그레스)를 TDD(Test-Driven Development) 방법론에 맞춰 4단계(Phase 1 ~ Phase 4)로 나누어 테스트 작성(Red) $\rightarrow$ 구현(Green) $\rightarrow$ 검증 및 리팩토링(Refactor) 순서로 진행하기 위해 작성되었습니다.

---

## 2. 4단계 TDD 태스크 로드맵 (4-Phase TDD Task Roadmap)

### 🧪 Phase 1: Auth & Connection REST API (Flow 1)
- **목표**: 로그인 자격검증 및 세션 토큰 발급/검증 API 구축 (`POST /api/v1/auth/login`, `GET /api/v1/auth/session`)
- **1-1. Red (테스트 작성)**:
  * `tests/test_detailed_runtime_flows.py::test_auth_login_success()`
  * `tests/test_detailed_runtime_flows.py::test_auth_login_invalid_credentials()`
  * `tests/test_detailed_runtime_flows.py::test_auth_session_validation()`
- **1-2. Green (기능 구현)**:
  * `src/main.py`: `POST /api/v1/auth/login` 및 `GET /api/v1/auth/session` 핸들러 구현
- **1-3. Refactor**: `python -m pytest tests/test_detailed_runtime_flows.py` 통과 검증

---

### 🧪 Phase 2: Chat Session & Preset Binding Management (Flow 2)
- **목표**: 대화 세션 CRUD 및 프리셋 스킬 바인딩 (< 200ms `NFR-PERF-04`) 구축 (`POST /api/v1/chat/sessions`, `GET /api/v1/chat/sessions`)
- **2-1. Red (테스트 작성)**:
  * `tests/test_detailed_runtime_flows.py::test_create_chat_session()`
  * `tests/test_detailed_runtime_flows.py::test_list_chat_sessions()`
  * `tests/test_detailed_runtime_flows.py::test_bind_preset_to_chat_session_latency()`
- **2-2. Green (기능 구현)**:
  * `src/main.py`: 세션 인메모리 저장소 및 `POST /api/v1/chat/sessions`, `GET /api/v1/chat/sessions` 핸들러 구현
  * `src/main.py`: `POST /api/v1/agent/bind-skill`에서 세션 상태 업데이트 연동
- **2-3. Refactor**: 바인딩 응답 속도 계측 및 `python -m pytest` 통과 검증

---

### 🧪 Phase 3: Token Streaming & Tool Call SSE API (Flow 3)
- **목표**: SSE(Server-Sent Events) 기반 LLM Chunk 및 Tool Call (`knowledge_search`) 이벤트 스트리밍 API 구축 (`POST /api/v1/chat/completions/stream`)
- **3-1. Red (테스트 작성)**:
  * `tests/test_detailed_runtime_flows.py::test_chat_completion_stream_chunks()`
  * `tests/test_detailed_runtime_flows.py::test_chat_completion_stream_tool_calling()`
- **3-2. Green (기능 구현)**:
  * `src/main.py`: `POST /api/v1/chat/completions/stream` SSE 핸들러 구현 (chunk_received, tool_call_start, final_answer 이벤트를 text/event-stream으로 발송)
- **3-3. Refactor**: SSE 포맷 준수 및 test suite 성공 확인

---

### 🧪 Phase 4: Ingestion Step Progress & Draft Preview UX (Flow 4)
- **목표**: 지식 추출 요청 시 3단계 상태 프로그레스(대화 분석 $\rightarrow$ Negative Knowledge 판별 $\rightarrow$ Draft 생성) 및 `.drafts/` 저장 수명주기 연동
- **4-1. Red (테스트 작성)**:
  * `tests/test_detailed_runtime_flows.py::test_knowledge_extract_progress_steps()`
  * `tests/test_detailed_runtime_flows.py::test_knowledge_extract_negative_knowledge_classification()`
- **4-2. Green (기능 구현)**:
  * `src/core/knowledge_ingestion_engine.py`: 3-step progress metadata 포함 response 구조 생성
  * `src/main.py`: `POST /api/v1/knowledge/extract` 응답에 `steps` 프로그레스 리스트 포함 반환
- **4-3. Refactor**: 전체 test suite (`python -m pytest`) 통과 검증

---

## 3. 검증 기준 (Verification Matrix)

| Test ID | 대상 기능 | 검증 기준 |
| :--- | :--- | :--- |
| `TEST-FLOW-01` | Auth Login & Session | 유효 자격증명 시 token 발급, 무효 시 401 반환, Session 조회 성공 |
| `TEST-FLOW-02` | Chat Session & Preset | 세션 생성 및 목록 조회, 바인딩 응답 시간 **< 200ms** (`NFR-PERF-04`) |
| `TEST-FLOW-03` | Token Streaming SSE | `text/event-stream` 헤더 발송 및 `chunk_received`, `tool_call_start` SSE 이벤트 포맷 검증 |
| `TEST-FLOW-04` | Ingestion Step Progress | 3단계 progress (`steps`) 및 `status: draft` 상태 `.drafts/` 파일 생성 검증 |
