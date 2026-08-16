# Knowledge Platform 실행 방법 및 모듈 기능 사용 설명서 (User Manual & Execution Guide)

> **Document ID**: `0816_user_manual_and_execution_guide`  
> **Date**: 2026-08-16  
> **Author**: Antigravity AI & Knowledge Architecture Team  
> **Reference Architecture**: [.doc/0816_knowledge_platform_architecture_spec.md](file:///home/chaehwan/bifacewiki/bifacewiki/.doc/0816_knowledge_platform_architecture_spec.md)  

---

## 1. 개요 및 비전

**Knowledge Platform**은 Human Knowledge와 AI Knowledge를 명확히 이원화하여 관리하며, **Physical Git Store (표준 마크다운 + Git)**와 **Logical Ref-DAG Graph Layer (메모리 + SQLite 2-Tier 인덱스)**를 결합한 차세대 지식 통합 플랫폼입니다.

---

## 2. 환경 설정 및 실행 방법 (Installation & Execution)

### 2.1 사전 요구 사항 (Prerequisites)
- **Python**: 3.10 이상
- **Git**: 2.30 이상
- **Node.js**: 18+ (Presentation UI 모듈 build/preview 시)

### 2.2 자동화 테스트 Suite 실행
플랫폼 전체 11개 모듈의 기능, 추적성 매트릭스, NFR 성능 타겟 지표, DAG 순환 방지 알고리즘 검증을 위한 테스트를 수행합니다.

```bash
# 1. 전체 단위 및 통합 테스트 실행 (10개 Test Case)
python -m pytest tests/ -v

# 2. NFR 성능 벤치마크 지표 전용 검증
python -m pytest tests/test_performance_benchmarks.py -v

# 3. Kahn's Algorithm 기반 Ref-DAG 순환 방지 전용 검증
python -m pytest tests/test_dag_cycle_prevention.py -v
```

---

## 3. 모듈별 기능 및 사용 설명서 (Core Feature Usage Manual)

### 1) Q&A 지식 추출 및 Atomic 작성 (`DSGN-CORE-INGEST`)
- **담당 파일**: [src/core/knowledge_ingestion_engine.py](file:///home/chaehwan/bifacewiki/bifacewiki/src/core/knowledge_ingestion_engine.py)
- **주요 기능**:
  - Q&A 대화 로그를 분석하여 1개 문서당 1개 주제만 다루는 **Atomic Markdown** 생성 (`NFR-MAINT-02`).
  - 실패/오류 경험 대화는 `type: negative_knowledge`로 자동 분류.
  - 생성된 지식은 Model Collapse 예방(`NFR-SEC-01`)을 위해 `.drafts/<node-id>.md` 경로에 `status: draft` 상태로 격리 저장.
- **Python 사용 예시**:
  ```python
  from src.core.knowledge_ingestion_engine import KnowledgeIngestionEngine, KnowledgeExtractRequestDTO

  engine = KnowledgeIngestionEngine(workspace_root="./")
  response = engine.extract_from_conversation(KnowledgeExtractRequestDTO(
      conversation_session_id="sess-001",
      raw_conversation_log="Q: Adapter memory leak 해결법? A: Close connection in finally block."
  ))
  print(f"Created Draft Node: {response.node_id} at {response.file_path}")
  ```

---

### 2) Ref-DAG 계층 인덱싱 & DAG 순환 방지 (`DSGN-INDEXER-DAG`)
- **담당 파일**: [src/indexer/ref_dag_indexer_engine.py](file:///home/chaehwan/bifacewiki/bifacewiki/src/indexer/ref_dag_indexer_engine.py)
- **주요 기능**:
  - Frontmatter 및 `[[Wikilinks]]` 구문을 AST 파싱하여 메모리(Tier-1) 및 SQLite 영속 캐시(Tier-2) 인덱스 구축.
  - Heading 섹션(`#`, `##`)을 `node-id#heading-slug` 형태의 서브블록 노드로 확장 파싱.
  - 파일 변경 이벤트 시 500ms Sliding Window 버퍼링(Debounce Queue) 후 차분 증분 갱신 (`NFR-PERF-02` < 50ms).
  - 신규 참조 엣지 추가 시 **Kahn's Topological Sort 알고리즘**을 통해 순환 참조(Circular Dependency) 감지 및 차단 (`NFR-RELI-03`).
- **Python 사용 예시**:
  ```python
  from src.indexer.ref_dag_indexer_engine import RefDAGIndexerEngine, Edge

  indexer = RefDAGIndexerEngine(db_path=":memory:")
  indexer.reindex_incremental(["knowledge/node-101.md"])

  # 순환 검증
  try:
      indexer.validate_dag_cycle(Edge(source="node-102", target="node-101", type="references"))
  except CircularDependencyException as e:
      print(f"Cycle detected and blocked: {e}")
  ```

---

### 3) Git 형상 관리 & Diff/Rollback (`DSGN-GIT-ADAPTER`)
- **담당 파일**: [src/storage/git_operations_adapter.py](file:///home/chaehwan/bifacewiki/bifacewiki/src/storage/git_operations_adapter.py)
- **주요 기능**:
  - CLI 없이 파일 기반 Git 커밋, 라인별 Visual Diff 계산, 커밋 롤백, Remote Push/Pull 동기화 지원 (`NFR-PERF-03` < 500ms).
  - Git Pre-commit 훅을 통해 승인되지 않은 `author_type: ai_generated` 지식이 `main` 브랜치로 커밋되는 시도 차단 (`NFR-SEC-01`).
  - OS Secure Keychain 연동으로 Git SSH/Token 원격 암호화 통신 (`NFR-SEC-02`).

---

### 4) 24/7 지식 자동 린팅 (`DSGN-LINTER-ENGINE`)
- **담당 파일**: [src/core/knowledge_linter_engine.py](file:///home/chaehwan/bifacewiki/bifacewiki/src/core/knowledge_linter_engine.py)
- **주요 기능**:
  - 깨진 링크(Broken Link), 고립 노드(Orphan Node), Frontmatter 메타 오차, 180일 이상 Stale Node, 상충 지식을 정적 자동 스캔.
  - 스캔 결과를 `LintAuditReportDTO` 리포트로 발간하여 승인 관문 UI로 전달.

---

### 5) 인간 검증 승인 관문 (`DSGN-APPROVAL-GATE`)
- **담당 파일**: [src/core/human_approval_gate_manager.py](file:///home/chaehwan/bifacewiki/bifacewiki/src/core/human_approval_gate_manager.py)
- **주요 기능**:
  - AI 생성 Draft 지식 검토 대기 큐 및 Diff 비교 기능 제공.
  - 인간 중개자(Human Broker) 승인 결정(`approve`) 시 `.drafts/`에서 `knowledge/` 경로로 파일 이동, `status: production` 전환, `main` 브랜치 병합 커밋 처리.
  - **`NFR-SEC-01` 엄격 통제**: AI 에이전트(`broker_id` = AI)가 스스로 지식을 승인하려는 시도는 권한 에러(PermissionError)로 완전 차단.

---

### 6) 그래프 리팩토링 & 수명주기 관리 (`DSGN-REFACTOR-ENGINE`)
- **담당 파일**: [src/core/graph_refactoring_engine.py](file:///home/chaehwan/bifacewiki/bifacewiki/src/core/graph_refactoring_engine.py)
- **주요 기능**:
  - 시맨틱 유사도 $\ge 0.90$ 인 파편화 중복 노드를 원자적 1개 노드로 통합(Merge)하는 리팩토링 플랜 제안.
  - 통합 시 기존 `[[Wikilinks]]` 참조 자동 리다이렉트 (Auto-redirection) 업데이트.
  - 낡고 폐기된 노드를 `archive/deprecated/` 디렉토리로 안전하게 이관 및 보관.

---

### 7) Universal LLM 어댑터 & Agent Tool 바인딩 (`DSGN-LLM-ADAPTER`, `DSGN-AGENT-BINDER`, `DSGN-AGENT-SKILL`)
- **담당 파일**: 
  - [src/agent/universal_llm_vendor_adapter.py](file:///home/chaehwan/bifacewiki/bifacewiki/src/agent/universal_llm_vendor_adapter.py)
  - [src/agent/skill_binding_middleware.py](file:///home/chaehwan/bifacewiki/bifacewiki/src/agent/skill_binding_middleware.py)
  - [src/agent/knowledge_retrieval_skill.py](file:///home/chaehwan/bifacewiki/bifacewiki/src/agent/knowledge_retrieval_skill.py)
- **주요 기능**:
  - OpenAI, Gemini, Claude, Local Ollama를 단일 인터페이스로 지원하며, 로컬 Ollama 호출 시 외부 라우팅을 차단하는 **Localhost Proxy Boundary (`NFR-SEC-03`)** 적용.
  - `.skill/` 내 스킬 정의 템플릿을 대화 세션에 동적 바인딩 (`NFR-PERF-04` < 200ms).
  - LLM의 `knowledge_search`, `knowledge_retrieve`, `knowledge_context_inject` Tool Call 지원. 오직 승인 완료된 `status: production` 지식만 Context로 조립 주입 (`NFR-PERF-05` < 500ms).

---

### 8) Git 관리 Dashboard UI & 외부 OS 프로토콜 연동 (`DSGN-UI-DASHBOARD`, `DSGN-LAUNCHER-PROTOCOL`)
- **담당 파일**:
  - [src/ui/git_management_dashboard.tsx](file:///home/chaehwan/bifacewiki/bifacewiki/src/ui/git_management_dashboard.tsx)
  - [src/ui/external_launcher_adapter.py](file:///home/chaehwan/bifacewiki/bifacewiki/src/ui/external_launcher_adapter.py)
- **주요 기능**:
  - Git 상태, 커밋 타임라인, Visual Line-by-Line Diff, 인간 승인 카드를 제공하는 React Web UI 컴포넌트.
  - `obsidian://open?vault=...&file=...` OS URI Scheme을 실행하여 Obsidian/Logseq vault 데스크톱 앱에서 지식 노드를 직접 시각화 오픈 (`NFR-COMP-01`).

---

## 4. 모듈 간 연동 시퀀스 (Ingestion -> Approval -> Main Branch Flow)

```
[1. Q&A 대화] ---> KnowledgeIngestionEngine ---> [.drafts/node-101.md (status: draft)]
                                                         |
                                                         v
                                              KnowledgeLinterEngine (24/7 Scan)
                                                         |
                                                         v
[2. Human Broker] ---> HumanApprovalGateManager ---> [Move to knowledge/ & Commit to main]
                                                         |
                                                         v
[3. LLM Agent] <--- KnowledgeRetrievalSkill <--- RefDAGIndexerEngine (status: production)
```
