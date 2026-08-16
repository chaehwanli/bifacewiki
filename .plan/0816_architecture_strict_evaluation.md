# Knowledge Platform Architecture Spec 4대 주체별 엄격 재평가 및 충돌 분석 보고서 (Plan/Draft)

> **Date**: 2026-08-16  
> **Evaluation Target**: [.doc/0816_knowledge_platform_architecture_spec.md](file:///home/chaehwan/bifacewiki/bifacewiki/.doc/0816_knowledge_platform_architecture_spec.md)  
> **Baseline Specs**: 
> - [.doc/0816_usecase_spec.md](file:///home/chaehwan/bifacewiki/bifacewiki/.doc/0816_usecase_spec.md)
> - [.doc/0816_requirements_and_nfr_spec.md](file:///home/chaehwan/bifacewiki/bifacewiki/.doc/0816_requirements_and_nfr_spec.md)  
> **Applied Role Skills**: [GEMINI.md](file:///home/chaehwan/bifacewiki/bifacewiki/GEMINI.md) 명시 4대 주체 스킬 (`architect`, `po`, `developer`, `qa`)

---

## 1. 평가 개요 및 종합 결론 (Executive Summary)

본 보고서는 개정 보완된 4대 주체별 스킬([.skill/architect/SKILL.md](file:///home/chaehwan/bifacewiki/bifacewiki/.skill/architect/SKILL.md), [.skill/po/SKILL.md](file:///home/chaehwan/bifacewiki/bifacewiki/.skill/po/SKILL.md), [.skill/developer/SKILL.md](file:///home/chaehwan/bifacewiki/bifacewiki/.skill/developer/SKILL.md), [.skill/qa/SKILL.md](file:///home/chaehwan/bifacewiki/bifacewiki/.skill/qa/SKILL.md))의 **엄격 평가 검증 지침(Strict Evaluation Rules)**을 100% 적용하여 [.doc/0816_knowledge_platform_architecture_spec.md](file:///home/chaehwan/bifacewiki/bifacewiki/.doc/0816_knowledge_platform_architecture_spec.md) 아키텍처 명세서를 재평가하고, **주체별 시각 차이 및 평가 충돌 요소(Role-based Conflicts & Trade-offs)**를 도출한 결과입니다.

### 🔴 종합 엄격 평가 결과: **41 / 100 점 (개념 설계 초안 수준 - 🔴 보완 필수)**

* **핵심 종합 평가**:
  - 현 아키텍처 사양서는 개념 수준(High-level)의 5계층 아키텍처 및 기본 블록 다이어그램을 제공하고 있으나, **실제 구현 시작(Coding Readiness) 및 계약 테스트(Contract Testing)를 수행하기 위한 동적 시퀀스, REST API 스키마, Git 거버넌스 전략이 결여**되어 있어 **개념 초안(Conceptual Outline) 수준인 41점**으로 평가되었습니다.

---

## 2. 4대 주체(Role & Skill)별 엄격 재평가 결과

| 주체 및 적용 스킬 | 핵심 평가 축 | 실질 점수 | 감점 및 판정 사유 (Defect Analysis) |
| :--- | :--- | :---: | :--- |
| 🏛️ **System Architect**<br/>(`architect` skill) | 계층 구조, 동적 시퀀스, Ref-DAG 알고리즘, NFR 제약 | **42 / 100** | • Mermaid Sequence Diagram 전무 (-15점)<br/>• Ref-DAG 캐시 무효화 및 순환 감지 알고리즘 부재 (-12점)<br/>• `status: production` 지식 격리 메커니즘 미비 (-11점) |
| 🎯 **Project Owner**<br/>(`po` skill) | 사업 목적, 수용 조건(AC), Git 브랜치 거버넌스, Model Collapse 통제 | **45 / 100** | • `Draft -> Production` Git 브랜치 전략 모호 (-7점)<br/>• Model Collapse 방지 통제 경계 기술적 미비 (-10점)<br/>• 비기술자용 대시보드 UX 상세 흐름 부재 (-8점) |
| 💻 **Core Developer**<br/>(`developer` skill) | 구현 가능성(Coding Readiness), REST API, DTO 스키마, 이벤트 규격 | **40 / 100** | • **구현 불가 판정**: REST API 엔드포인트, DTO 페이로드 스키마, 메서드 시그니처가 0개로 문서만으로 개발 시작 불가 (-20점) |
| 🧪 **QA Lead / Test팀**<br/>(`qa` skill) | `DSGN` 추적성, API 계약 테스트, NFR 측정 가능성 | **38 / 100** | • `DSGN-xxx` 모듈 식별 태그 미병기로 추적 단절 (-5점)<br/>• API 계약 스키마 미정의로 Mock 스텁 설계 불가 (-15점)<br/>• NFR 측정 포인트 미지정 (-12점) |

---

## 3. 주체별 평가 충돌 및 시각 차이 분석 (Role-based Conflicts & Trade-offs)

4대 주체별 스킬 검증 항목을 적용하는 과정에서 **주체 간 시각 차이로 인해 발생한 3대 아키텍처적 충돌 포인트(Conflict Points)**입니다.

```mermaid
graph LR
    Architect["🏛️ Architect\n(완벽한 격리 & DAG 정합성)"] <-->|Conflict 1: Git 전략| PO["🎯 PO\n(운영 용이성 & 단순 UX)"]
    Architect <-->|Conflict 2: 명세 상세도| Dev["💻 Developer\n(구현용 API/DTO 규격)"]
    QA["🧪 QA Lead\n(DSGN 태그 & 계약 테스트)| <-->|Conflict 3: 추적성| Dev
```

### ⚡ 충돌 1: Project Owner (PO) vs System Architect — [Git 거버넌스 및 브랜치 격리 전략]
- **PO 시각**: 비기술자인 인간 승인자(Knowledge Broker)가 복잡한 Git 브랜치 Merge 충돌을 겪지 않도록 **단일 `main` 브랜치 + 물리적 `/drafts/` 디렉토리 + Frontmatter `status: draft` 속성** 관리를 선호함.
- **Architect 시각**: 승인되지 않은 AI 지식이 프로덕션 DAG 인덱스에 오염되는 것을 구조적으로 막기 위해 **Git의 물리적 `draft` 브랜치와 `main` 브랜치 분리 및 Pull Request 병합 전략**을 요구함.
- **아키텍처 명세서의 현 상태 (충돌 사유)**: 명세서 다이어그램이 `Draft / Archive / Main`을 모호하게 표기하여 PO의 운영 편의성과 Architect의 엄격한 데이터 격리 요구를 둘 다 만족시키지 못함 (**PO 45점 / Architect 42점 주요 감점 요인**).

### ⚡ 충돌 2: Core Developer vs System Architect — [추상적 계층 모델 vs 구현용 API/DTO 명세]
- **Architect 시각**: 고수준 계층 모듈화(5계층 모듈 뷰) 및 컴포넌트 간 상호작용 개념이 잡혀있으므로 아키텍처적 구조 완성도를 인정함 (42점).
- **Developer 시각**: 백엔드/프론트엔드 개발에 즉시 착수하려면 `POST /api/v1/knowledge/extract`의 Request/Response DTO 스키마, WebSocket/이벤트 규격, 메서드 파라미터가 명시되어야 하나 단 1개도 없어 **"구현 불가능(Un-implementable)"**로 판정함 (**40점 낙제점**).

### ⚡ 충돌 3: QA Lead vs Developer & Architect — [모듈 명칭 체계 및 계약 테스트(Contract Test) 가능성]
- **Architect & Dev 시각**: 구현 관점의 기능적 클래스/컴포넌트 명칭 (`GitManagerComponent`, `LLMVendorAdapter`)을 표에 기술함.
- **QA Lead 시각**: `0816_requirements_and_nfr_spec.md`에 공식 정의된 `DSGN-UI-DASHBOARD`, `DSGN-LLM-ADAPTER` 식별 태그가 아키텍처 표에 병기되지 않아 **REQ-DSGN-TEST 추적 매트릭스가 단절**되었으며, API Payload 계약이 미정의되어 **통합/계약 테스트 스텁 작성이 불가능**하다고 판정함 (**38점 최저점**).

---

## 4. 40점 대 탈피를 위한 주체별 보완 요청사항 (Action Roadmap)

본 아키텍처 명세서를 4대 주체 모두가 승인 가능한 **90점 이상 확정 사양서**로 격상시키기 위해 다음 4가지 핵심 보완 작업을 제안합니다.

1. **[Architect 보완] Section 1.3 Sequence Diagram 2종 추가**:
   - Scenario A: 지식 추출 -> Draft 등록 -> Linter 검사 -> 승인 -> Git Main 커밋 동적 시퀀스
   - Scenario B: Agent 지식 탐색 (`knowledge_search`) 및 Context 주입 시퀀스
2. **[PO/Architect 합의 보완] Section 1.4 Git Strategy 명시**:
   - `main` 브랜치 단일 운영 + `/drafts/`, `/production/`, `/archive/` 디렉토리 및 Frontmatter `status` 관리 전략 확정
3. **[Developer 보완] Section 2.1 API & DTO 명세 추가**:
   - 16개 모듈별 REST API 엔드포인트 URL, DTO JSON 스키마, 핵심 메서드 파라미터 명시
4. **[QA 보완] Section 2.1 `DSGN` 태그 병기 & Section 4 NFR 테스트 지점 명시**:
   - `DSGN-CORE-INGEST` 등 요구사항 식별 태그 병기 및 NFR 성능/보안 검증 포인트 지정
