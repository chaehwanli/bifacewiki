"""
Automated Test Suite for Traceability Matrix (TEST-UC001-01 ~ TEST-UC011-01)
"""

import os
import shutil
import tempfile
import pytest

from src.storage.git_operations_adapter import GitOperationsAdapter
from src.indexer.ref_dag_indexer_engine import RefDAGIndexerEngine, CircularDependencyException, Edge
from src.core.knowledge_ingestion_engine import KnowledgeIngestionEngine, KnowledgeExtractRequestDTO
from src.core.knowledge_linter_engine import KnowledgeLinterEngine
from src.core.human_approval_gate_manager import HumanApprovalGateManager, ApprovalDecisionDTO
from src.core.graph_refactoring_engine import GraphRefactoringEngine
from src.agent.universal_llm_vendor_adapter import UniversalLLMVendorAdapter, VendorConfigDTO, LLMInvokeRequestDTO
from src.agent.skill_binding_middleware import SkillBindingMiddleware
from src.agent.knowledge_retrieval_skill import KnowledgeRetrievalSkill
from src.ui.external_launcher_adapter import ExternalLauncherAdapter


@pytest.fixture
def temp_workspace():
    tmp_dir = tempfile.mkdtemp()
    yield tmp_dir
    shutil.rmtree(tmp_dir)


def test_uc001_ingestion(temp_workspace):
    """TEST-UC001-01: Q&A Extraction and Atomic Markdown creation."""
    engine = KnowledgeIngestionEngine(temp_workspace)
    req = KnowledgeExtractRequestDTO(
        conversation_session_id="sess-001",
        raw_conversation_log="How to resolve NullPointerException in adapter?"
    )
    res = engine.extract_from_conversation(req)
    assert res.node_id is not None
    assert res.frontmatter.status == "draft"
    assert os.path.exists(os.path.join(temp_workspace, res.file_path))


def test_uc002_indexer_and_cycle_prevention(temp_workspace):
    """TEST-UC002-01: Ref-DAG Indexing & Kahn's Cycle Prevention."""
    indexer = RefDAGIndexerEngine()

    # Create dummy node files
    f1 = os.path.join(temp_workspace, "node-1.md")
    f2 = os.path.join(temp_workspace, "node-2.md")
    with open(f1, 'w') as f:
        f.write("---\nid: node-1\ntitle: N1\ntype: concept\nstatus: production\nauthor_type: human_authored\n---\n# N1\nLink to [[node-2]]")
    with open(f2, 'w') as f:
        f.write("---\nid: node-2\ntitle: N2\ntype: concept\nstatus: production\nauthor_type: human_authored\n---\n# N2\nContent")

    indexer.reindex_incremental([f1, f2])
    assert "node-1" in indexer.nodes
    assert "node-2" in indexer.nodes

    # Try creating cycle: node-2 -> node-1
    with pytest.raises(CircularDependencyException):
        indexer.validate_dag_cycle(Edge(source="node-2", target="node-1", type="references"))


def test_uc009_approval_gate_and_nfr_sec_01(temp_workspace):
    """TEST-UC009-01 & NFR-SEC-01: Human Approval Gate & AI Block."""
    git_adapter = GitOperationsAdapter(temp_workspace)
    # Init git repo
    git_adapter._run_cmd(["init"])
    git_adapter._run_cmd(["config", "user.name", "Test"])
    git_adapter._run_cmd(["config", "user.email", "test@test.com"])

    indexer = RefDAGIndexerEngine()
    gate = HumanApprovalGateManager(temp_workspace, git_adapter, indexer)

    # Ingest draft node
    ingest = KnowledgeIngestionEngine(temp_workspace)
    res = ingest.extract_from_conversation(KnowledgeExtractRequestDTO(
        conversation_session_id="sess-002",
        raw_conversation_log="Draft solution for memory leak"
    ))

    # Verify pending queue
    pending = gate.get_pending_approvals()
    assert len(pending) == 1

    # Verify AI Self-Approval block (NFR-SEC-01)
    with pytest.raises(PermissionError):
        gate.decide_approval(ApprovalDecisionDTO(
            node_id=res.node_id,
            decision="approve",
            broker_id="ai_agent_bot"
        ))

    # Human broker approves
    result = gate.decide_approval(ApprovalDecisionDTO(
        node_id=res.node_id,
        decision="approve",
        broker_id="broker_john"
    ))
    assert result.success is True
    assert os.path.exists(os.path.join(temp_workspace, result.target_file_path))


def test_uc005_ollama_sandbox_isolation():
    """TEST-UC005-01 & NFR-SEC-03: Ollama Localhost Proxy Sandbox Isolation."""
    adapter = UniversalLLMVendorAdapter(initial_vendor="ollama")
    assert adapter.config.endpoint_url == "http://127.0.0.1:11434"


def test_uc005_antigravity_vendor_switch():
    """TEST-UC005-02: Google Antigravity CLI LLM Vendor Switch support."""
    adapter = UniversalLLMVendorAdapter(initial_vendor="openai")
    cfg = VendorConfigDTO(vendor_code="antigravity", model_name="antigravity-agent-v1")
    assert adapter.switch_vendor("antigravity", cfg) is True
    assert adapter.active_vendor == "antigravity"

