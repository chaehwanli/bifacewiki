# 주체별 (Role-based) .skill/ 스킬 모듈 정의서 (Plan/Draft)

> **Date**: 2026-08-16  
> **Subject**: Knowledge Platform 과제 수행 주체(System Architect, PO, Tech Lead/Dev, QA Lead)별 `.skill/` 스킬 정의  
> **Target Reference**: [GEMINI.md](file:///home/chaehwan/bifacewiki/bifacewiki/GEMINI.md)

---

## 1. 개요 및 의도 Clarification

본 문서의 목적은 본 과제(Knowledge Platform)의 설계 및 구현에 참여하는 **4대 핵심 협력/검토 주체(Role)**별로, 에이전트 작업 수행 시 참고/활용할 **.skill/ 디렉토리 내의 주체별 전문 스킬 모듈(`SKILL.md`)**을 정의하는 것입니다.

---

## 2. 협력 및 검토 주체별 .skill/ 스킬 구성안

### 1) System Architect 주체용 스킬: `.skill/architect/SKILL.md`
- **스킬명**: `architect`
- **담당 주체**: System Architect / Knowledge Architect
- **핵심 역할 및 수행 작업**:
  - 전체 시스템 아키텍처 사양서(`0816_knowledge_platform_architecture_spec.md`) 작성 및 갱신
  - Dual-Layer (Physical Git Store + Logical Ref-DAG) 및 Zettelkasten 지식 모델 설계
  - `DSGN` 모듈 규격, REST API 인터페이스, 데이터 및 제어 시퀀스 흐름(Sequence Flow) 정의
  - NFR 제약조건 명세 (Model Collapse 예방 `status: production` 조회 격리, Ref-DAG 캐시 무효화 메커니즘 등)

### 2) Project Owner (PO) 주체용 스킬: `.skill/po/SKILL.md`
- **스킬명**: `po`
- **담당 주체**: Project Owner (PO) / Knowledge Broker
- **핵심 역할 및 수행 작업**:
  - 비즈니스 및 지식 거버넌스 정책 수립 (Human-AI Authority Boundary 정의)
  - 지식 수명주기 승인 정책 (`draft` -> `production` -> `archive`) 수립 및 인간 승인 관문(Human Approval Gate) 비즈니스 규칙 준수 검증
  - REQ/NFR 요구사항 수용 조건 (Acceptance Criteria) 수립 및 Git Management UI 가치 검증

### 3) Tech Lead & Core Developer 주체용 스킬: `.skill/developer/SKILL.md`
- **스킬명**: `developer`
- **담당 주체**: Tech Lead & Core Developer
- **핵심 역할 및 수행 작업**:
  - Core Engine 계층 (`KnowledgeIngestionEngine`, `KnowledgeLinterEngine`, `GraphRefactoringEngine`) 구현
  - AST 파서 (`WikilinkParser`, Frontmatter Header Parser) 및 Ref-DAG In-Memory 인덱서 구축
  - Low-level Git 연동 어댑터 (`GitOperationsAdapter`) 및 Universal LLM Vendor 어댑터 (`LLMVendorAdapter`) 개발
  - Frontend Web UI (Git Sync Dashboard, Visual Diff Viewer, Approval Gate Widget) 개발

### 4) QA Lead & 기능 Test팀 주체용 스킬: `.skill/qa/SKILL.md`
- **스킬명**: `qa`
- **담당 주체**: QA Lead & Functional Test Team
- **핵심 역할 및 수행 작업**:
  - `REQ-DSGN-TEST` 추적성 매트릭스 기반 단위/통합/E2E 검증 시나리오 설계
  - LLM Tool Calling 계약 테스트 (Contract Test) 및 Mocking 테스트 스텁 개발
  - NFR 성능 타겟 지표 (지식 추출 < 3s, 그래프 파싱 < 1s, Git 커밋 < 500ms) 및 보안 (Ollama 사내망 데이터 격리) 수치 검증

---

## 3. GEMINI.md 반영 계획

`GEMINI.md` 내 `## skill` 섹션을 아래와 같이 4대 주체별 스킬 모듈 구조로 정리합니다.

```markdown
## skill
.skill폴더에 정리해 놓은 주체별 스킬을 참고하여 작업을 수행해주세요.

- **[architect](file:///home/chaehwan/bifacewiki/bifacewiki/.skill/architect/SKILL.md)**: System Architect 주체용 (전체 아키텍처, Ref-DAG 모델링, 인터페이스 및 NFR 제약조건 정의 스킬)
- **[po](file:///home/chaehwan/bifacewiki/bifacewiki/.skill/po/SKILL.md)**: Project Owner 주체용 (요구사항 수용조건 검증, 지식 거버넌스 및 승인 관문 정책 정의 스킬)
- **[developer](file:///home/chaehwan/bifacewiki/bifacewiki/.skill/developer/SKILL.md)**: Developer 주체용 (Core 모듈 구현, AST 파서, Git 및 LLM 어댑터 개발 스킬)
- **[qa](file:///home/chaehwan/bifacewiki/bifacewiki/.skill/qa/SKILL.md)**: QA/Test 주체용 (REQ-DSGN-TEST 추적성 검증, 통합/계약 테스트 시나리오 및 NFR 검증 스킬)
```
