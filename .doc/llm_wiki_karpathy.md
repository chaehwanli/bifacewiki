# Andrej Karpathy - LLM Wiki (llm-wiki.md)

- **Source URL**: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
- **Title**: llm-wiki: A pattern for building personal knowledge bases using LLMs

---

## 1. 개요 (Overview)
LLM을 활용하여 개인 지식 기반(Personal Knowledge Base)을 구축하고 지속적으로 유지보수하는 패턴입니다. 
기존 RAG(Retrieval-Augmented Generation) 방식은 질문 시점에만 원본 문서를 검색하여 답변을 재구성하므로 지식이 누적되지 않는 한계가 있습니다. 반면, **LLM Wiki**는 LLM이 불변의 소스를 바탕으로 지식을 추출하고 지속적으로 상호 참조(Cross-reference)가 연결된 Markdown 형태의 위키 지식 기반을 구축 및 관리합니다.

## 2. 3계층 아키텍처 (Three Layers Architecture)
1. **Raw Sources (원천 소스)**: 불변(Immutable) 문서 컬렉션 (기사, 논문, 데이터 파일 등). LLM은 읽기 전용으로 접근.
2. **The Wiki (위키 레이어)**: LLM이 완전히 소유하고 생성/수정하는 Markdown 파일 디렉토리 (요약, 개념/엔티티 페이지, 비교 분석 문서 등).
3. **The Schema (스키마)**: 위키의 구조, 이름 규칙, 수집/질의/검사 워크플로를 규정한 가이드 파일 (예: `CLAUDE.md`, `AGENTS.md`).

## 3. 주요 운영 방식 (Operations)
- **Ingest (수집 및 통합)**: 새 소스를 원천 컬렉션에 추가하면 LLM이 이를 분석하여 위키에 요약 페이지 작성, 인덱스 업데이트, 연관 엔티티/개념 페이지를 수정 및 확장.
- **Query (질의 및 탐색)**: 위키를 바탕으로 질의응답을 진행하고, 축적된 통찰이나 분석 결과는 다시 위키의 새 페이지로 저장하여 지식 누적.
- **Lint (무결성 검사)**: 주기적으로 위키 전체의 모순, 오래된(Stale) 주장, 고립된(Orphan) 페이지, 누락된 링크를 점검하고 개선.

## 4. 색인 및 기록 (Indexing & Logging)
- **`index.md`**: 콘텐츠 카탈로그 파일. 범주별 목록과 링크, 한 줄 요약 제공.
- **`log.md`**: 수집, 질의, 린트 작업 이력을 관리하는 시간 순서의 추가 전용(Append-only) 로그.

## 5. 의의 (Significance)
지식 기반 구축 시 지루한 유지보수(Bookkeeping) 및 정리 작업을 LLM에게 전담시키고, 인간은 자료 선택, 탐색 방향 결정, 질의 및 통찰 형성에 집중할 수 있도록 돕습니다.
