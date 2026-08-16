# Role별 Skill 엄격 평가 검증 항목 보완 계획 (Plan/Draft)

> **Date**: 2026-08-16  
> **Subject**: `.skill/` 내 4대 주체별 스킬(`architect`, `po`, `developer`, `qa`)에 엄격하고 구체적인 실질 평가 지침 보완  
> **Target Files**: 
> - [.skill/architect/SKILL.md](file:///home/chaehwan/bifacewiki/bifacewiki/.skill/architect/SKILL.md)
> - [.skill/po/SKILL.md](file:///home/chaehwan/bifacewiki/bifacewiki/.skill/po/SKILL.md)
> - [.skill/developer/SKILL.md](file:///home/chaehwan/bifacewiki/bifacewiki/.skill/developer/SKILL.md)
> - [.skill/qa/SKILL.md](file:///home/chaehwan/bifacewiki/bifacewiki/.skill/qa/SKILL.md)

---

## 1. 보완 배경 및 목적

기존 `.skill/` 내 스킬 지침이 표면적인 서술 항목 포함 여부만을 확인하도록 완만하게 기술되어 있어, 구현 가능성(Implementation Readiness)이나 테스트 가능성(Testability)이 결여된 하이레벨 개요 문서에 대해 높은 점수를 부여하는 오류가 발생하였습니다.

따라서 4대 주체별 스킬 파일(`SKILL.md`)에 **실체적 구현 및 엄격한 검증을 강제하는 '무관용 감점 기준 및 엄격 평가 검증 항목(Strict Evaluation Checklist)'**을 보완 개정합니다.

---

## 2. 주체별 스킬 보완 개정 내용

### 2.1 `architect` 스킬 보완 ([.skill/architect/SKILL.md](file:///home/chaehwan/bifacewiki/bifacewiki/.skill/architect/SKILL.md))
- **추가할 엄격 평가 기준**:
  - **시퀀스 다이어그램 필수화**: 핵심 런타임 흐름(Q&A -> Draft -> Linter -> Approval -> Git Commit)에 대한 Sequence Diagram 누락 시 아키텍처 불통과 처리.
  - **NFR 기술 메커니즘 구체성**: Model Collapse 방지를 위한 `status: production` 전용 조회 필터링 아키텍처 및 Ref-DAG 인덱스 무효화(Cache Invalidation) 이벤트 명세 필수 검증.
  - **DAG 순환 감지 알고리즘**: Kahn's Algo / DFS cycle detection 서술 유무 검증.

### 2.2 `po` 스킬 보완 ([.skill/po/SKILL.md](file:///home/chaehwan/bifacewiki/bifacewiki/.skill/po/SKILL.md))
- **추가할 엄격 평가 기준**:
  - **형상 관리 / Git 브랜치 전략 명확성**: `Draft -> Production` 승인 시 Git 브랜치(`draft` branch vs `main` single branch) 및 디렉토리 관리 구조가 명시되지 않은 사양서는 비승인 처리.
  - **Human-AI Authority Boundary 구체성**: AI 생성 지식의 결함 유출을 차단하는 접근 통제 경계 및 거버넌스 아키텍처 검증.

### 2.3 `developer` 스킬 보완 ([.skill/developer/SKILL.md](file:///home/chaehwan/bifacewiki/bifacewiki/.skill/developer/SKILL.md))
- **추가할 엄격 평가 기준**:
  - **구현 시작 가능성 (Coding Readiness)**: 문서만 보고 즉시 개발에 착수할 수 없는 사양서(REST API 엔드포인트, DTO 스키마, 메서드 파라미터, 이벤트 규격 미비)는 **40점 이하 (구현 불가)** 판정.
  - **모듈 계약(Contract) 구체성**: 백엔드 파서 및 어댑터의 구체적 입출력 규격 검증.

### 2.4 `qa` 스킬 보완 ([.skill/qa/SKILL.md](file:///home/chaehwan/bifacewiki/bifacewiki/.skill/qa/SKILL.md))
- **추가할 엄격 평가 기준**:
  - **REQ-DSGN-TEST 추적성 태그 필수화**: 요구사항 명세서의 `DSGN-xxx` 모듈 ID가 아키텍처 문서 표에 명시되지 않으면 추적 단절(Un-trackable) 처리.
  - **계약 테스트 및 Mock 스텁 설계 가능성**: API 엔드포인트/이벤트 규격 미정의 시 계약 테스트(Contract Test) 불가능 판정.
  - **NFR 측정 기준 연동**: NFR 수치 타겟(성능 < 3s, < 1s, 보안 격리)과 연동되는 아키텍처 검증 포인트 확인.
