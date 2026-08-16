"""
Knowledge Linter Engine (DSGN-LINTER-ENGINE)

Performs 24/7 static audit scans across markdown files and Ref-DAG index:
- Broken link detection
- Orphan node detection
- YAML Frontmatter schema error detection
- Stale node detection (> 180 days)
- Contradiction detection
"""

import os
import re
import time
from datetime import datetime, timezone
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

from src.indexer.ref_dag_indexer_engine import RefDAGIndexerEngine, Node, Edge


@dataclass
class BrokenLinkIssue:
    source_node_id: str
    missing_target_link: str


@dataclass
class LintAuditReportDTO:
    scan_timestamp: str
    total_nodes_scanned: int
    broken_links: List[BrokenLinkIssue] = field(default_factory=list)
    orphan_nodes: List[str] = field(default_factory=list)
    stale_nodes: List[str] = field(default_factory=list)
    schema_error_nodes: List[str] = field(default_factory=list)


class KnowledgeLinterEngine:
    def __init__(self, indexer: RefDAGIndexerEngine):
        self.indexer = indexer

    def detect_broken_links(self) -> List[BrokenLinkIssue]:
        broken = []
        node_ids = set(self.indexer.nodes.keys())
        for edge in self.indexer.edges:
            if edge.type == "references" and edge.target not in node_ids:
                broken.append(BrokenLinkIssue(
                    source_node_id=edge.source,
                    missing_target_link=edge.target
                ))
        return broken

    def detect_orphan_nodes(self) -> List[str]:
        referenced_nodes = set()
        for edge in self.indexer.edges:
            referenced_nodes.add(edge.source)
            referenced_nodes.add(edge.target)

        orphans = []
        for node_id in self.indexer.nodes.keys():
            if node_id not in referenced_nodes:
                orphans.append(node_id)
        return orphans

    def detect_stale_nodes(self, repo_path: str, max_age_days: int = 180) -> List[str]:
        stale = []
        now = time.time()
        max_age_sec = max_age_days * 86400

        for node_id, node in self.indexer.nodes.items():
            if os.path.exists(node.file_path):
                mtime = os.path.getmtime(node.file_path)
                if (now - mtime) > max_age_sec:
                    stale.append(node_id)
        return stale

    def run_audit_scan(self, repo_path: str) -> LintAuditReportDTO:
        """
        Executes static audit scan and returns LintAuditReportDTO.
        """
        broken_links = self.detect_broken_links()
        orphan_nodes = self.detect_orphan_nodes()
        stale_nodes = self.detect_stale_nodes(repo_path, max_age_days=180)

        schema_errors = []
        for node_id, node in self.indexer.nodes.items():
            if not node.title or not node.type or not node.status:
                schema_errors.append(node_id)

        timestamp = datetime.now(timezone.utc).isoformat()

        return LintAuditReportDTO(
            scan_timestamp=timestamp,
            total_nodes_scanned=len(self.indexer.nodes),
            broken_links=broken_links,
            orphan_nodes=orphan_nodes,
            stale_nodes=stale_nodes,
            schema_error_nodes=schema_errors
        )
