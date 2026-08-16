# Use Case Spec 문서 분리 기획 (Plan)

> **Date**: 2026-08-16  
> **Subject**: [.doc/0816_knowledge_platform_architecture_spec.md](file:///home/chaehwan/bifacewiki/bifacewiki/.doc/0816_knowledge_platform_architecture_spec.md)에서 Use Case 세부 명세를 별도의 `.doc` 사양 문서로 분리  
> **Status**: Completed (완료)

---

## 1. 개요 및 배경

기존 [.doc/0816_knowledge_platform_architecture_spec.md](file:///home/chaehwan/bifacewiki/bifacewiki/.doc/0816_knowledge_platform_architecture_spec.md) 문서에 아키텍처 구조(전체 구조, 모듈 뷰)와 함께 UC-001 ~ UC-011 세부 유스케이스 명세가 통합되어 있어 문서의 분량이 과대해지고 관심사 분리(Separation of Concerns)가 필요한 상태입니다.

따라서 UC-001 ~ UC-011 세부 유스케이스 명세를 별도의 확정 레퍼런스 문서 [.doc/0816_usecase_spec.md](file:///home/chaehwan/bifacewiki/bifacewiki/.doc/0816_usecase_spec.md)로 분리하여 다음과 같이 관리 체계를 정립합니다.

- **[.doc/0816_knowledge_platform_architecture_spec.md](file:///home/chaehwan/bifacewiki/bifacewiki/.doc/0816_knowledge_platform_architecture_spec.md)**: overall architecture, 모듈 뷰, 계층 구조, 콤포넌트 간 상호작용 및 시퀀스 중심
- **[.doc/0816_usecase_spec.md](file:///home/chaehwan/bifacewiki/bifacewiki/.doc/0816_usecase_spec.md)**: UC-001 ~ UC-011 개별 세부 유스케이스 명세서 및 유스케이스 매트릭스 요약
- **[.doc/0816_requirements_and_nfr_spec.md](file:///home/chaehwan/bifacewiki/bifacewiki/.doc/0816_requirements_and_nfr_spec.md)**: 기능/비기능 요구사항(REQ/NFR) 및 추적성(Traceability) 매트릭스

---

## 2. 작업 상세 계획 및 진행 현황

### Step 1: [.doc/0816_usecase_spec.md](file:///home/chaehwan/bifacewiki/bifacewiki/.doc/0816_usecase_spec.md) 신규 생성 `[완료]`
- 문서 ID: `0816_usecase_spec`
- 헤더 메타데이터 구성 (관련 아키텍처 문서 및 요구사항 문서 링크 포함)
- **1. 개요 및 분류 체계**: Ingestion, Structure, Storage, Management, Platform, Agent, Retrieval, Governance, Approval, Lifecycle, Exploration
- **2. Use Case Detail Specifications**: UC-001 ~ UC-011 세부 표준 명세 표 전량 수록 (Postcondition, Scope, Primary/Secondary Actor, Precondition, Trigger, Main/Alt/Exception Flow, Rule, API/UI, NFR, Traceability 포함)
- **3. Use Case Summary Matrix**: UC-001 ~ UC-011 전체 매트릭스 및 REQ/DSGN/TEST 추적 연동 표 수록

### Step 2: [.doc/0816_knowledge_platform_architecture_spec.md](file:///home/chaehwan/bifacewiki/bifacewiki/.doc/0816_knowledge_platform_architecture_spec.md) 수정 `[완료]`
- 문서 헤더의 `Related Documents`에 `0816_usecase_spec.md` 추가
- Section 3의 긴 UC-001 ~ UC-011 상세 표 목록을 제거하고, [.doc/0816_usecase_spec.md](file:///home/chaehwan/bifacewiki/bifacewiki/.doc/0816_usecase_spec.md)로의 참조 요약 섹션으로 경량화
- Section 4 추적성 매트릭스 요약을 `0816_usecase_spec.md`로 이관하고 아키텍처 관점의 모듈 연결 요약으로 재구성

### Step 3: [.doc/0816_requirements_and_nfr_spec.md](file:///home/chaehwan/bifacewiki/bifacewiki/.doc/0816_requirements_and_nfr_spec.md) 참조 갱신 `[완료]`
- 문서 헤더 및 추적성 섹션에 `0816_usecase_spec.md` 상호 참조 링크 추가

---

## 3. 검토 및 검증 결과

- **절대 경로 clickable link (`file:///...`) 검증**: `0816_usecase_spec.md`, `0816_knowledge_platform_architecture_spec.md`, `0816_requirements_and_nfr_spec.md` 간 모든 파일 링크 상호 동작 확인 완료.
- **문서 간 상호 추적성(Traceability) 일관성 확인**:
  - `UC-001` ~ `UC-011` <-> `REQ-INGEST-01` ~ `REQ-INTEG-OBS-01`
  - `DSGN-CORE-INGEST` ~ `DSGN-LAUNCHER-PROTOCOL`
  - `TEST-UC001-01` ~ `TEST-UC011-01`
  - `NFR-PERF-01` ~ `NFR-COMP-01`
  - 모든 11개 유스케이스 및 요구사항 식별 태그 100% 교차 검증 완료.

