"""
Human Approval Gate Manager (DSGN-APPROVAL-GATE)

Manages pending draft review queue, enforces Model Collapse prevention (NFR-SEC-01),
and handles human broker approval/rejection decisions to promote drafts from .drafts/ to knowledge/.
"""

import os
import re
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

from src.storage.git_operations_adapter import GitOperationsAdapter
from src.indexer.ref_dag_indexer_engine import RefDAGIndexerEngine


@dataclass
class PendingApprovalNodeDTO:
    node_id: str
    file_path: str
    title: str
    type: str
    author_type: str
    extracted_markdown: str


@dataclass
class ApprovalDecisionDTO:
    node_id: str
    decision: str  # approve, reject, request_revision
    broker_id: str
    review_note: Optional[str] = None


@dataclass
class ApprovalResultDTO:
    success: bool
    node_id: str
    decision: str
    commit_hash: Optional[str] = None
    target_file_path: Optional[str] = None
    message: str = ""


class HumanApprovalGateManager:
    def __init__(self, workspace_root: str, git_adapter: GitOperationsAdapter, indexer: RefDAGIndexerEngine):
        self.workspace_root = os.path.abspath(workspace_root)
        self.drafts_dir = os.path.join(self.workspace_root, ".drafts")
        self.prod_dir = os.path.join(self.workspace_root, "knowledge")
        self.git_adapter = git_adapter
        self.indexer = indexer
        os.makedirs(self.prod_dir, exist_ok=True)

    def get_pending_approvals(self) -> List[PendingApprovalNodeDTO]:
        """
        Retrieves list of pending draft nodes awaiting human review.
        """
        pending = []
        if not os.path.exists(self.drafts_dir):
            return pending

        for file_name in os.listdir(self.drafts_dir):
            if file_name.endswith('.md'):
                file_path = os.path.join(self.drafts_dir, file_name)
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                node_id = os.path.splitext(file_name)[0]
                title_match = re.search(r'title:\s*"(.*?)"', content) or re.search(r'title:\s*(.*)', content)
                type_match = re.search(r'type:\s*(.*)', content)
                author_match = re.search(r'author_type:\s*(.*)', content)

                pending.append(PendingApprovalNodeDTO(
                    node_id=node_id,
                    file_path=os.path.relpath(file_path, self.workspace_root),
                    title=title_match.group(1).strip() if title_match else node_id,
                    type=type_match.group(1).strip() if type_match else "solution",
                    author_type=author_match.group(1).strip() if author_match else "ai_generated",
                    extracted_markdown=content
                ))
        return pending

    def decide_approval(self, decision_dto: ApprovalDecisionDTO) -> ApprovalResultDTO:
        """
        Processes Human Broker approval decision.
        NFR-SEC-01: Must be called only by human broker.
        """
        if not decision_dto.broker_id or decision_dto.broker_id.startswith("ai_agent"):
            raise PermissionError("NFR-SEC-01 Violation: AI agents are strictly prohibited from approving draft nodes.")

        draft_file = os.path.join(self.drafts_dir, f"{decision_dto.node_id}.md")
        if not os.path.exists(draft_file):
            return ApprovalResultDTO(
                success=False,
                node_id=decision_dto.node_id,
                decision=decision_dto.decision,
                message=f"Draft node '{decision_dto.node_id}' not found."
            )

        if decision_dto.decision == "reject":
            os.remove(draft_file)
            return ApprovalResultDTO(
                success=True,
                node_id=decision_dto.node_id,
                decision="reject",
                message="Draft node rejected and deleted."
            )

        if decision_dto.decision == "approve":
            # 1. Update status to production and append approved_by metadata
            with open(draft_file, 'r', encoding='utf-8') as f:
                content = f.read()

            updated_content = re.sub(r'status:\s*draft', 'status: production', content)
            updated_content = re.sub(r'(---.*?\n)', f'\\1approved_by: "{decision_dto.broker_id}"\n', updated_content, count=1, flags=re.DOTALL)

            # 2. Move file from .drafts/ to knowledge/
            target_file = os.path.join(self.prod_dir, f"{decision_dto.node_id}.md")
            with open(target_file, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            os.remove(draft_file)

            rel_target_path = os.path.relpath(target_file, self.workspace_root)

            # 3. Git commit & promote to main
            commit_hash = self.git_adapter.commit(
                file_paths=[rel_target_path],
                message=f"feat: promote {decision_dto.node_id} to production by {decision_dto.broker_id}",
                author=f"{decision_dto.broker_id} <broker@bifacewiki.org>"
            )

            # 4. Trigger reindex
            self.indexer.reindex_incremental([target_file])

            return ApprovalResultDTO(
                success=True,
                node_id=decision_dto.node_id,
                decision="approve",
                commit_hash=commit_hash,
                target_file_path=rel_target_path,
                message="Node approved, promoted to production, and committed."
            )

        return ApprovalResultDTO(
            success=False,
            node_id=decision_dto.node_id,
            decision=decision_dto.decision,
            message=f"Unsupported decision option '{decision_dto.decision}'."
        )
