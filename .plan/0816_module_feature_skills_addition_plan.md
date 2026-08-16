# Knowledge Platform 모듈 기능별 Skill 추가 계획 (Plan/Draft)

> **Document ID**: `0816_module_feature_skills_plan`  
> **Date**: 2026-08-16  
> **Author**: Antigravity AI & Knowledge Architecture Team  
> **Reference Document**: [.doc/0816_knowledge_platform_architecture_spec.md](file:///home/chaehwan/bifacewiki/bifacewiki/.doc/0816_knowledge_platform_architecture_spec.md)  
> **Target Path**: `.skill/` 디렉토리 내 모듈 기능별 스킬 정의 및 [GEMINI.md](file:///home/chaehwan/bifacewiki/bifacewiki/GEMINI.md) 반영  

---

## 1. 추진 배경 및 목적

Knowledge Platform 전체 아키텍처 명세서(`0816_knowledge_platform_architecture_spec.md`)에 정의된 11개 설계 모듈(`DSGN-CORE-INGEST` ~ `DSGN-LAUNCHER-PROTOCOL`)의 기능별 구현 및 LLM 에이전트 연동을 체계적으로 수행하기 위하여, **모듈의 기능별 전용 Skill**을 `.skill/` 디렉토리에 추가 정의합니다.

기존 `.skill/` 디렉토리에는 4대 역할별 스킬(`architect`, `po`, `developer`, `qa`)이 구성되어 있었으나, 모듈 개발 및 런타임 Agent Tool Execution 시 각 모듈 기능의 핵심 사양(API, DTO, NFR, Agent Tool Calling 규약, 구현 체크리스트)을 직접 참고할 수 있도록 **8대 모듈 기능별 스킬 모듈**을 세분화하여 신설합니다.

---

## 2. 8대 모듈 기능별 Skill 구조 및 매핑 정의

| 스킬 ID / 폴더명 | 대상 DSGN 모듈 ID | 핵심 기능 및 구현 대상 | LLM Agent Tool | 주요 NFR / 제약조건 |
| :--- | :--- | :--- | :--- | :--- |
| **`ingestion`** | `DSGN-CORE-INGEST` | Q&A 지식 추출, Atomic Markdown 작성, Minimal Frontmatter 검증, Negative Knowledge 분류 | `knowledge_extract` | Latency < 3s (`NFR-PERF-01`), 원자성 보장 (`NFR-MAINT-02`) |
| **`indexer_dag`** | `DSGN-INDEXER-DAG` | Ref-DAG 메모리/SQLite Tier-2 persistent 캐시 인덱싱, Sub-block 파싱, 500ms 디바운스, Kahn's algorithm DAG 순환 방지 | `knowledge_search` | Cold Start < 500ms, Incremental < 50ms (`NFR-PERF-02`), 순환 방지 (`NFR-RELI-03`) |
| **`git_adapter`** | `DSGN-GIT-ADAPTER` | 파일 기반 Git 명령어(commit, diff, rollback, push/pull) 래퍼, OS Keychain security | `knowledge_git_commit` | Local Commit < 500ms (`NFR-PERF-03`), SSH/Token 보안 (`NFR-SEC-02`) |
| **`linter_engine`** | `DSGN-LINTER-ENGINE` | 깨진 링크, Orphan Node, 스키마 오류, 180일 Stale Node 정적 24/7 자동 린팅 | `knowledge_audit_scan` | 자동 린팅 및 Audit 리포트 발행 (`NFR-RELI-02`) |
| **`approval_gate`** | `DSGN-APPROVAL-GATE` | Draft 격리 (`.drafts/`), 인간 승인 관문 Decision API, `main` 브랜치 병합 커밋 | `knowledge_get_pending_approvals` | **`NFR-SEC-01` 제약**: AI 자가 승인 엄격 금지! (`decide_approval` AI 차단) |
| **`refactor_engine`** | `DSGN-REFACTOR-ENGINE` | 중복 노드 통합(Merge) 제안 ($\ge 0.90$), Wikilink auto-redirect, Archive 이관 | `knowledge_propose_merge` | 지식 수명주기 관리 (`NFR-MAINT-02`) |
| **`agent_binder`** | `DSGN-LLM-ADAPTER`<br/>`DSGN-AGENT-BINDER`<br/>`DSGN-AGENT-SKILL` | Vendor-agnostic LLM 어댑터 (Ollama localhost proxy), 동적 YAML 스킬 바인딩, Context 주입 | `agent_bind_skill`<br/>`knowledge_retrieve`<br/>`knowledge_context_inject` | Skill 바인딩 < 200ms (`NFR-PERF-04`), Context 주입 < 500ms (`NFR-PERF-05`), Proxy Isolation (`NFR-SEC-03`) |
| **`presentation_ui`**| `DSGN-UI-DASHBOARD`<br/>`DSGN-LAUNCHER-PROTOCOL`| Git GUI Dashboard, Line-by-Line Visual Diff Viewer, Approval Widget, Obsidian URI scheme launcher | - | UX 시각화 및 external app 연동 (`NFR-COMP-01`) |

---

## 3. 실행 단계 계획 (Execution Strategy)

1. **`.skill/` 모듈 기능별 SKILL.md 작성**:
   - `.skill/ingestion/SKILL.md`
   - `.skill/indexer_dag/SKILL.md`
   - `.skill/git_adapter/SKILL.md`
   - `.skill/linter_engine/SKILL.md`
   - `.skill/approval_gate/SKILL.md`
   - `.skill/refactor_engine/SKILL.md`
   - `.skill/agent_binder/SKILL.md`
   - `.skill/presentation_ui/SKILL.md`
2. **`GEMINI.md` 스킬 섹션 업데이트**:
   - 신규 추가된 8개 모듈 기능별 스킬을 `GEMINI.md` 내 `## skill` 목록에 등록하여 시스템 전체에서 참조 가능하도록 반영.
3. **종합 구현 계획서 (`implementation_plan.md`) 작성**:
   - `0816_knowledge_platform_architecture_spec.md` 및 추가된 스킬을 기반으로 전체 11개 모듈 구현 순서, 의존성 관계, 단계별 검증 방안(Automated Tests & Manual Verification) 명시.
