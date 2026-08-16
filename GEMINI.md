## purpose
이 프로젝트는 Knowledge를 human knowledge 와 AI Knowledge 로 구분하고 각 지식의 특성을 이용하여 llm 이 최적의 Knowledge를 선택적으로 사용할 수 있도록 하는 것이 목적입니다. 
The purpose of this project is to categorize Knowledge into Human Knowledge and AI Knowledge, leveraging the characteristics of each so that the LLM can selectively utilize the optimal Knowledge.

## plan
.plan/ (기획 & 아이디어 메모):
작업 진행 과정에서의 생각 정리, 진행 로드맵, 브레인스토밍 메모, 검토용 초안 (Draft)
.plan폴더에 생각할 내용을 정리하면서 진행해주세요. 문서 파일명은 MMDD_subject.md 형식을 사용해 저장해주세요.

## reference (.doc)
.doc/ (확정 레퍼런스 & 사양서):
구상이 완료되어 실제 구현 및 시스템의 진실의 원천(Source of Truth)으로 활용할 확정 아키텍처 사양서, 요구사항 정의서, 유스케이스 명세서 (Final Specifications)
.doc폴더에 정리해 놓은 자료를 참고해주세요.


## skill
.skill폴더에 정리해 놓은 주체별/모듈 기능별 스킬을 참고하여 작업을 수행해주세요. (Please refer to the role-based and module-based skills compiled in the `.skill` folder.)

### 1) 역할/주체별 스킬 (Role-Based Skills)
- **[architect](file:///home/chaehwan/bifacewiki/bifacewiki/.skill/architect/SKILL.md)**: System Architect 주체용 (전체 아키텍처 사양서, Ref-DAG 모델링, 모듈 인터페이스 및 NFR 제약조건 정의 스킬)
- **[po](file:///home/chaehwan/bifacewiki/bifacewiki/.skill/po/SKILL.md)**: Project Owner 주체용 (요구사항 수용조건 검증, 지식 거버넌스 및 승인 관문 정책 정의 스킬)
- **[developer](file:///home/chaehwan/bifacewiki/bifacewiki/.skill/developer/SKILL.md)**: Tech Lead & Core Developer 주체용 (Core 모듈 구현, AST 파서, Git 및 LLM 어댑터 개발 스킬)
- **[qa](file:///home/chaehwan/bifacewiki/bifacewiki/.skill/qa/SKILL.md)**: QA Lead & Functional Test팀 주체용 (REQ-DSGN-TEST 추적성 검증, 통합/계약 테스트 시나리오 및 NFR 검증 스킬)

### 2) 모듈 기능별 스킬 (Module-Feature Skills)
- **[ingestion](file:///home/chaehwan/bifacewiki/bifacewiki/.skill/ingestion/SKILL.md)**: `DSGN-CORE-INGEST` Knowledge Ingestion Engine (Q&A 추출, Atomic 문서, Minimal Schema, Negative Knowledge)
- **[indexer_dag](file:///home/chaehwan/bifacewiki/bifacewiki/.skill/indexer_dag/SKILL.md)**: `DSGN-INDEXER-DAG` Ref-DAG Indexer (Sub-block 파싱, SQLite Tier-2 캐시, 500ms 디바운스, Kahn's DAG 순환 감지)
- **[git_adapter](file:///home/chaehwan/bifacewiki/bifacewiki/.skill/git_adapter/SKILL.md)**: `DSGN-GIT-ADAPTER` Git Operations Adapter (Commit, Diff, Rollback, Push/Pull, OS Keychain)
- **[linter_engine](file:///home/chaehwan/bifacewiki/bifacewiki/.skill/linter_engine/SKILL.md)**: `DSGN-LINTER-ENGINE` Knowledge Linter Engine (Broken link, Orphan node, Schema error, 180d Stale, Contradiction 24/7 static audit)
- **[approval_gate](file:///home/chaehwan/bifacewiki/bifacewiki/.skill/approval_gate/SKILL.md)**: `DSGN-APPROVAL-GATE` Human Approval Gate Manager (`.drafts/` 격리, Model Collapse 예방 `NFR-SEC-01`, 인간 승인 API)
- **[refactor_engine](file:///home/chaehwan/bifacewiki/bifacewiki/.skill/refactor_engine/SKILL.md)**: `DSGN-REFACTOR-ENGINE` Graph Refactoring Engine (파편화 노드 통합 제안 $\ge 0.90$, Wikilink auto-redirect, Archive 이관)
- **[agent_binder](file:///home/chaehwan/bifacewiki/bifacewiki/.skill/agent_binder/SKILL.md)**: `DSGN-LLM-ADAPTER`, `DSGN-AGENT-BINDER`, `DSGN-AGENT-SKILL` LLM Adapter & Agent Binder (Universal LLM, Ollama proxy `NFR-SEC-03`, 동적 스킬 바인딩, Context 주입)
- **[presentation_ui](file:///home/chaehwan/bifacewiki/bifacewiki/.skill/presentation_ui/SKILL.md)**: `DSGN-UI-DASHBOARD`, `DSGN-LAUNCHER-PROTOCOL` Presentation UI & Launcher (Git Dashboard, Visual Diff, Approval Widget, Obsidian URI launcher)

## agent
.agent폴더에 정리해 놓은 에이전트를 참고해주세요.
Please refer to the agents compiled in the `.agent` folder.

