# LLM Service Skill 타당성 분석 보고서 (LLM Skill Appropriateness Matrix)

> **Document ID**: `0816_llm_skill_appropriateness_matrix`  
> **Date**: 2026-08-16  
> **Target Doc**: [.doc/0816_knowledge_platform_architecture_spec.md](file:///home/chaehwan/bifacewiki/bifacewiki/.doc/0816_knowledge_platform_architecture_spec.md)  
> **Author**: Knowledge Platform Architecture Team  

---

## 1. 개요 (Overview)

Knowledge Platform의 11개 설계 모듈(`DSGN-CORE-INGEST` ~ `DSGN-LAUNCHER-PROTOCOL`)의 기능들을 분석하여, **LLM Service의 Agent Skill(Tool Calling)로 제공하기에 타당한 기능(Skill-Appropriate)**과 **시스템 백그라운드/보안/인간 관문 영역으로 직접 제공해서는 안 되는 기능(Non-Skill / System-Internal)**을 분류한 명세 매트릭스입니다.

---

## 2. 모듈별 기능의 LLM Skill 타당성 분석 표 (LLM Skill vs Platform Internal Matrix)

| 모듈 ID | 기능 / 메서드명 | LLM Skill 제공 타당성 | 타당 여부 판단 사유 및 주체 구분 |
| :--- | :--- | :---: | :--- |
| **DSGN-CORE-INGEST** | `extract_from_conversation` | **O (Skill 타당)** | 대화 분석, 핵심 요약, Negative Knowledge 분류 등 **AI의 맥락 인지 및 지식 추출 추론 능력이 필수로 요구됨**. Skill명: `knowledge_extract` |
| | `parse_frontmatter_schema` | **X (시스템 전용)** | 마크다운 텍스트 규격 정적 파싱 로직. 단순 파서 유틸리티로 LLM 추론 불필요. |
| **DSGN-INDEXER-DAG** | `get_related_subgraph` | **O (Skill 타당)** | LLM이 질의에 관련된 지식 그래프 탐색 시 노드 연관 탐색 도구로 활용. Skill명: `knowledge_search` |
| | `reindex_incremental` | **X (시스템 전용)** | 파일 시스템 변경 시 SQLite 캐시 갱신을 담당하는 백그라운드 인덱서 데몬. |
| | `debounce_file_events` | **X (시스템 전용)** | OS level inotify 500ms Sliding Window 버퍼링 로직. 순수 하위 인프라 기능. |
| | `validate_dag_cycle` | **X (시스템 전용)** | Kahn's Algorithm 기반 정적 수학적 그래프 검증 로직. 엔진 내부 하드검증. |
| **DSGN-GIT-ADAPTER** | `commit` / `rollback` | **O (Skill 타당)** | Agent가 지식 수정/병합 후 원자적 Git 커밋 메세지를 구조화하여 발송할 때 활용. Skill명: `knowledge_git_commit` |
| | `sync_remote` | **X (시스템 전용)** | SSH/Keychain 인증 기반 원격 Push/Pull 통신. 대시보드 및 백그라운드 동기화 몫. |
| **DSGN-UI-DASHBOARD** | `render_status_widget` 등 | **X (시스템 전용)** | React/Web Frontend UI Visual 렌더링 component. LLM Tool 호출 대상 아님. |
| **DSGN-LLM-ADAPTER** | `invoke` | **X (시스템 전용)** | LLM 호출 그 자체를 담당하는 최하위 커넥터 코어 API. |
| | `switch_vendor` | **X (시스템 전용)** | 시스템 관리자 및 UI 설정 영역. 보안상 LLM이 임의로 벤더를 바꾸지 못하도록 격리. |
| **DSGN-AGENT-BINDER** | `bind_skill` | **O (Skill 타당)** | 대화 맥락 변경 시 Agent 스스로 필요한 스킬 셋을 동적 바인딩 요청할 때 활용. Skill명: `agent_bind_skill` |
| **DSGN-AGENT-SKILL** | `knowledge_search` | **O (Skill 타당)** | LLM 질의 키워드 기반 Ref-DAG 지식 노드 검색 스킬. Skill명: `knowledge_search` |
| | `knowledge_retrieve` | **O (Skill 타당)** | 특정 노드 ID 및 엣지 연관 문서 상세 조회 스킬. Skill명: `knowledge_retrieve` |
| | `knowledge_context_inject` | **O (Skill 타당)** | 획득한 지식을 프롬프트 Context 포맷으로 정밀 조립 주입 스킬. Skill명: `knowledge_context_inject` |
| **DSGN-LINTER-ENGINE**| `run_audit_scan` | **O (Skill 타당)** | 깨진 링크, Orphan Node, Contradiction 탐지 후 리포트 작성을 Agent가 주도. Skill명: `knowledge_audit_scan` |
| | `detect_broken_links` | **X (시스템 전용)** | Linter 엔진 내부 정적 문자열 정규식 파서. |
| **DSGN-APPROVAL-GATE**| `get_pending_approvals`| **O (Skill 타당)** | Agent 또는 인간 중개자가 승인 대기 노드 목록 및 Diff를 조회할 때 사용. Skill명: `knowledge_get_pending_approvals` |
| | `decide_approval` | **X (Skill 불가/보안차단)** | **[NFR-SEC-01 핵심 제약]** AI 생성 지식을 AI 스스로 승인(Self-Approval)하면 Model Collapse 발생! 오직 인간 중개자(Human Broker) REST API/UI 전용. |
| **DSGN-REFACTOR-ENGINE**| `propose_merge_plan` | **O (Skill 타당)** | 파편화 지식 분석 후 통합(Merge) 플랜 초안을 추론 작성하는 스킬. Skill명: `knowledge_propose_merge` |
| | `execute_merge` / `prune` | **X (시스템 전용)** | 인간 승인 후 확정된 리팩토링 트랜잭션을 백엔드에서 일괄 파일 이동/커밋하는 로직. |
| **DSGN-LAUNCHER-PROTOCOL**| `launch_external_tool`| **X (시스템 전용)** | 클라이언트 OS URI Scheme (`obsidian://open`) 실행. Web UI 프론트엔드 전용 버튼 이벤트. |

---

## 3. 핵심 분류 원칙 및 판단 가이드라인 (Design Principles)

### 🟢 LLM Skill 제공이 타당한 기능 (Skill-Appropriate Functions)
1. **AI 추론 및 자유 형식 입력 분석이 필요한 기능**: Q&A 대화 추출, 지식 정합성/모순 탐지, 리팩토링/병합 플랜 제안.
2. **동적 탐색 및 지식 Context 조립 기능**: Ref-DAG 키워드 검색, 노드 이웃 엣지 탐색, Context 주입.
3. **Agent 작업 수행 결과 영속화**: 구조화된 Git 커밋 메세지 작성 및 저장 요청.

### 🔴 LLM Skill 제공이 타당하지 않은 기능 (Platform Internal Functions)
1. **인간 승인 거버넌스 및 보안 차단 기능 (`NFR-SEC-01`)**: `decide_approval` (AI의 자가 승인 금지).
2. **순수 결정론적 시스템 백그라운드 데몬 / 알고리즘**: Kahn's DAG 순환 참조 알고리즘, inotify 500ms 디바운싱 큐, SQLite 영속 캐시 증분 파서.
3. **클라이언트 OS / 프론트엔드 전용 UI 인터랙션**: Obsidian OS URI scheme 호출, React 컴포넌트 렌더링, LLM Vendor 선택 설정.
