"""
Knowledge Ingestion Engine (DSGN-CORE-INGEST)

Parses Q&A conversation sessions, extracts Atomic Markdown documents,
validates Minimal Schema, classifies negative knowledge, and persists draft files to .drafts/.
"""

import os
import re
import time
import uuid
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass
class KnowledgeExtractRequestDTO:
    conversation_session_id: str
    raw_conversation_log: str
    classification_hints: List[str] = field(default_factory=list)


@dataclass
class FrontmatterDTO:
    id: str
    title: str
    type: str  # concept, solution, negative_knowledge, architecture
    status: str  # draft
    author_type: str  # ai_generated, human_authored


@dataclass
class KnowledgeExtractResponseDTO:
    node_id: str
    file_path: str
    frontmatter: FrontmatterDTO
    extracted_markdown: str


class KnowledgeIngestionEngine:
    def __init__(self, workspace_root: str):
        self.workspace_root = os.path.abspath(workspace_root)
        self.drafts_dir = os.path.join(self.workspace_root, ".drafts")
        os.makedirs(self.drafts_dir, exist_ok=True)

    def validate_atomic_constraint(self, content: str) -> bool:
        """
        Validates atomic constraint (NFR-MAINT-02).
        Single document must cover 1 topic (e.g. heading level 1 count <= 1).
        """
        h1_count = len(re.findall(r'^#\s+', content, re.MULTILINE))
        return h1_count <= 1

    def parse_frontmatter_schema(self, raw_md: str) -> FrontmatterDTO:
        """
        Extracts YAML Frontmatter metadata into FrontmatterDTO.
        """
        match = re.search(r'^---\s*\n(.*?)\n---\s*\n', raw_md, re.DOTALL)
        if not match:
            raise ValueError("Invalid markdown format: missing frontmatter block.")

        meta = {}
        for line in match.group(1).splitlines():
            if ':' in line:
                k, v = line.split(':', 1)
                meta[k.strip()] = v.strip().strip('"\'')

        return FrontmatterDTO(
            id=meta.get('id', str(uuid.uuid4())[:8]),
            title=meta.get('title', 'Untitled Knowledge'),
            type=meta.get('type', 'solution'),
            status=meta.get('status', 'draft'),
            author_type=meta.get('author_type', 'ai_generated')
        )

    def extract_from_conversation(self, request: KnowledgeExtractRequestDTO) -> KnowledgeExtractResponseDTO:
        """
        Parses conversation log and extracts Atomic Markdown + Minimal Frontmatter.
        Latency target: < 3s (NFR-PERF-01).
        """
        start_time = time.time()

        log = request.raw_conversation_log.lower()
        is_negative = "error" in log or "failed" in log or "bug" in log or "antipattern" in log
        knowledge_type = "negative_knowledge" if is_negative else "solution"

        node_id = f"node-{uuid.uuid4().hex[:8]}"
        title_line = request.raw_conversation_log.strip().splitlines()[0][:50] if request.raw_conversation_log else "Q&A Extraction"
        clean_title = re.sub(r'[^\w\s\-]', '', title_line).strip() or "QA Knowledge Node"

        markdown_body = f"""---
id: {node_id}
title: "{clean_title}"
type: {knowledge_type}
status: draft
author_type: ai_generated
---

# {clean_title}

## Problem / Question
{request.raw_conversation_log}

## Resolution / Summary
Extracted resolution from Q&A session {request.conversation_session_id}.
"""

        # Enforce atomic constraint
        if not self.validate_atomic_constraint(markdown_body):
            raise ValueError("Atomic constraint violation: Document contains multiple top-level topics.")

        file_name = f"{node_id}.md"
        file_path = os.path.join(self.drafts_dir, file_name)

        # Write to .drafts/ (NFR-SEC-01 isolation)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(markdown_body)

        frontmatter = self.parse_frontmatter_schema(markdown_body)

        elapsed = time.time() - start_time
        if elapsed > 3.0:
            print(f"[Warning] Ingestion latency target exceeded: {elapsed:.3f}s")

        return KnowledgeExtractResponseDTO(
            node_id=node_id,
            file_path=os.path.relpath(file_path, self.workspace_root),
            frontmatter=frontmatter,
            extracted_markdown=markdown_body
        )
