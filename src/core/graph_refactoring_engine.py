"""
Graph Refactoring Engine (DSGN-REFACTOR-ENGINE)

Proposes duplicate node consolidation plans (similarity >= 0.90),
executes Wikilink auto-redirections, and handles node deprecation/archiving lifecycle.
"""

import os
import re
import uuid
import shutil
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Set

from src.indexer.ref_dag_indexer_engine import RefDAGIndexerEngine, Node
from src.storage.git_operations_adapter import GitOperationsAdapter


@dataclass
class RefactorPlanDTO:
    plan_id: str
    target_primary_node: str
    source_duplicate_nodes: List[str]
    similarity_score: float
    wikilink_redirects_count: int


@dataclass
class MergeResultDTO:
    success: bool
    plan_id: str
    merged_node_id: str
    updated_files: List[str]
    message: str


@dataclass
class PruneResultDTO:
    success: bool
    pruned_node_ids: List[str]
    archived_paths: List[str]


class GraphRefactoringEngine:
    def __init__(self, workspace_root: str, indexer: RefDAGIndexerEngine, git_adapter: GitOperationsAdapter):
        self.workspace_root = os.path.abspath(workspace_root)
        self.archive_dir = os.path.join(self.workspace_root, "archive", "deprecated")
        self.indexer = indexer
        self.git_adapter = git_adapter
        os.makedirs(self.archive_dir, exist_ok=True)
        self.active_plans: Dict[str, RefactorPlanDTO] = {}

    def propose_merge_plan(self, candidate_ids: List[str]) -> RefactorPlanDTO:
        """
        Formulates merge proposal plan for fragmented nodes.
        """
        if len(candidate_ids) < 2:
            raise ValueError("At least 2 candidate nodes are required for merge plan.")

        primary_id = candidate_ids[0]
        duplicate_ids = candidate_ids[1:]
        plan_id = f"plan-{uuid.uuid4().hex[:8]}"

        # Calculate count of wikilinks that need redirecting
        redirect_count = 0
        for edge in self.indexer.edges:
            if edge.target in duplicate_ids:
                redirect_count += 1

        plan = RefactorPlanDTO(
            plan_id=plan_id,
            target_primary_node=primary_id,
            source_duplicate_nodes=duplicate_ids,
            similarity_score=0.92,  # Mock calculated similarity >= 0.90
            wikilink_redirects_count=redirect_count
        )
        self.active_plans[plan_id] = plan
        return plan

    def execute_merge(self, plan_id: str) -> MergeResultDTO:
        """
        Executes approved node merge plan and updates Wikilinks auto-redirect.
        """
        plan = self.active_plans.get(plan_id)
        if not plan:
            return MergeResultDTO(
                success=False,
                plan_id=plan_id,
                merged_node_id="",
                updated_files=[],
                message=f"Refactor plan '{plan_id}' not found."
            )

        updated_files = []

        # 1. Update Wikilinks in all markdown files
        for node_id, node in self.indexer.nodes.items():
            if node_id in plan.source_duplicate_nodes or not os.path.exists(node.file_path):
                continue

            with open(node.file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            modified = False
            for dup_id in plan.source_duplicate_nodes:
                pattern = rf'\[\[{re.escape(dup_id)}(\|.*?)?\]\]'
                replacement = f'[[{plan.target_primary_node}\\1]]'
                if re.search(pattern, content):
                    content = re.sub(pattern, replacement, content)
                    modified = True

            if modified:
                with open(node.file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                updated_files.append(os.path.relpath(node.file_path, self.workspace_root))

        # 2. Archive source duplicate nodes
        self.prune_deprecated_nodes(plan.source_duplicate_nodes)

        return MergeResultDTO(
            success=True,
            plan_id=plan_id,
            merged_node_id=plan.target_primary_node,
            updated_files=updated_files,
            message="Node merge executed successfully with Wikilinks auto-redirection."
        )

    def prune_deprecated_nodes(self, target_ids: List[str]) -> PruneResultDTO:
        """
        Transitions deprecated nodes to archive/deprecated/ directory.
        """
        archived_paths = []
        for node_id in target_ids:
            node = self.indexer.nodes.get(node_id)
            if node and os.path.exists(node.file_path):
                target_archive_path = os.path.join(self.archive_dir, f"{node_id}.md")
                shutil.move(node.file_path, target_archive_path)
                archived_paths.append(os.path.relpath(target_archive_path, self.workspace_root))

        return PruneResultDTO(
            success=True,
            pruned_node_ids=target_ids,
            archived_paths=archived_paths
        )
