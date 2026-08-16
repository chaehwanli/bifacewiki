"""
Knowledge Retrieval Skill (DSGN-AGENT-SKILL)

Provides Agent Tool Calling interface for LLMs to search Ref-DAG nodes,
retrieve markdown contents, and assemble verified prompt contexts (NFR-SEC-01).
"""

import os
import time
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

from src.indexer.ref_dag_indexer_engine import RefDAGIndexerEngine, Node, SubGraphDTO


@dataclass
class NodeSummaryDTO:
    id: str
    title: str
    type: str
    status: str


@dataclass
class KnowledgeContextDTO:
    node_id: str
    title: str
    content: str
    related_edges: List[str] = field(default_factory=list)


class KnowledgeRetrievalSkill:
    def __init__(self, indexer: RefDAGIndexerEngine):
        self.indexer = indexer

    def knowledge_search(self, query: str, filter_tags: Optional[List[str]] = None) -> List[NodeSummaryDTO]:
        """
        Searches Ref-DAG nodes matching query string with status: production filter (NFR-SEC-01).
        Latency target: < 500ms (NFR-PERF-05).
        """
        start_time = time.time()

        matched = []
        query_lower = query.lower()

        for node_id, node in self.indexer.nodes.items():
            # NFR-SEC-01 constraint: Only production nodes are searchable by AI
            if node.status != "production" or node.is_subblock:
                continue

            if query_lower in node.id.lower() or query_lower in node.title.lower():
                matched.append(NodeSummaryDTO(
                    id=node.id,
                    title=node.title,
                    type=node.type,
                    status=node.status
                ))

        elapsed = (time.time() - start_time) * 1000
        if elapsed > 500:
            print(f"[Warning] Context search latency target exceeded: {elapsed:.2f}ms")

        return matched

    def knowledge_retrieve(self, node_id: str, depth: int = 1) -> KnowledgeContextDTO:
        """
        Retrieves Markdown content and edge relations for node_id.
        """
        subgraph = self.indexer.get_related_subgraph(node_id, depth=depth, filter_status="production")
        node = self.indexer.nodes.get(node_id)

        if not node or node.status != "production":
            raise PermissionError(f"NFR-SEC-01 Isolation: Access to non-production node '{node_id}' is restricted.")

        content = ""
        if os.path.exists(node.file_path):
            with open(node.file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

        edges_str = [f"{e.source} -> {e.target} ({e.type})" for e in subgraph.edges]

        return KnowledgeContextDTO(
            node_id=node.id,
            title=node.title,
            content=content,
            related_edges=edges_str
        )

    def knowledge_context_inject(self, context: KnowledgeContextDTO) -> str:
        """
        Formats retrieved KnowledgeContextDTO into a structured System Prompt Context string.
        """
        return f"""### Verified Knowledge Context [ID: {context.node_id}]
**Title**: {context.title}
**Relations**: {', '.join(context.related_edges) if context.related_edges else 'None'}

```markdown
{context.content}
```
"""
