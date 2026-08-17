"""
Dashboard Enhancement Unit & Integration Tests (tests/test_dashboard_enhancements.py)

Tests Git Operations Adapter enhancements, LLM Vendor settings API, Ref-DAG Edges & Refactoring APIs,
and Knowledge Search Playground endpoints according to 0816_dashboard_tdd_task_plan.md.
"""

import os
import json
import unittest

from src.storage.git_operations_adapter import GitOperationsAdapter, CommitDTO
from src.agent.universal_llm_vendor_adapter import UniversalLLMVendorAdapter, VendorConfigDTO
from src.indexer.ref_dag_indexer_engine import RefDAGIndexerEngine, Node, Edge
from src.core.graph_refactoring_engine import GraphRefactoringEngine
from src.main import KnowledgePlatformAPIHandler


class TestGitOperationsAdapterEnhancements(unittest.TestCase):
    def setUp(self):
        self.workspace_root = os.getcwd()
        self.adapter = GitOperationsAdapter(self.workspace_root)

    def test_git_adapter_get_history(self):
        """Phase 1: Test GitOperationsAdapter.get_history(limit) returns CommitDTO list."""
        history = self.adapter.get_history(limit=5)
        self.assertIsInstance(history, list)
        if len(history) > 0:
            commit = history[0]
            self.assertIsInstance(commit, CommitDTO)
            self.assertTrue(len(commit.commit_hash) > 0)
            self.assertIsNotNone(commit.author)
            self.assertIsNotNone(commit.message)

    def test_git_adapter_get_diff(self):
        """Phase 1: Test GitOperationsAdapter.get_diff() returns DiffResultDTO."""
        diff = self.adapter.get_diff("HEAD~1", "HEAD")
        self.assertIsNotNone(diff.diff_text)
        self.assertIsInstance(diff.files_changed, list)


class TestLLMVendorAdapterEnhancements(unittest.TestCase):
    def setUp(self):
        self.adapter = UniversalLLMVendorAdapter(initial_vendor="openai")

    def test_switch_vendor_valid(self):
        """Phase 2: Test switching active vendor to gemini, claude, ollama, antigravity."""
        for vendor in ["gemini", "claude", "antigravity"]:
            cfg = VendorConfigDTO(vendor_code=vendor, model_name=f"{vendor}-model")
            success = self.adapter.switch_vendor(vendor, cfg)
            self.assertTrue(success)
            self.assertEqual(self.adapter.active_vendor, vendor)

    def test_ollama_sandbox_isolation_nfr_sec_03(self):
        """Phase 2: Test NFR-SEC-03 localhost proxy enforcement for Ollama."""
        cfg = VendorConfigDTO(vendor_code="ollama", model_name="llama3")
        self.adapter.switch_vendor("ollama", cfg)
        self.assertEqual(self.adapter.active_vendor, "ollama")
        self.assertEqual(self.adapter.config.endpoint_url, "http://127.0.0.1:11434")


class TestGraphRefactoringEngineEnhancements(unittest.TestCase):
    def setUp(self):
        self.workspace_root = os.getcwd()
        self.indexer = RefDAGIndexerEngine()
        self.git_adapter = GitOperationsAdapter(self.workspace_root)
        self.refactor = GraphRefactoringEngine(self.workspace_root, self.indexer, self.git_adapter)

    def test_propose_merge_plan(self):
        """Phase 3: Test proposing duplicate node merge plan."""
        self.indexer.nodes["node-a"] = Node(id="node-a", title="Node A", type="concept", status="production", author_type="human", file_path="knowledge/node-a.md", content_hash="hash-a")
        self.indexer.nodes["node-b"] = Node(id="node-b", title="Node B Duplicate", type="concept", status="production", author_type="human", file_path="knowledge/node-b.md", content_hash="hash-b")

        plan = self.refactor.propose_merge_plan(["node-a", "node-b"])
        self.assertEqual(plan.target_primary_node, "node-a")
        self.assertIn("node-b", plan.source_duplicate_nodes)
        self.assertGreaterEqual(plan.similarity_score, 0.90)


class TestRESTAPIHandlers(unittest.TestCase):
    """Integration test suite verifying newly added REST API handlers in src/main.py."""

    def test_handler_initialization(self):
        self.assertIsNotNone(KnowledgePlatformAPIHandler.git_adapter)
        self.assertIsNotNone(KnowledgePlatformAPIHandler.llm_adapter)
        self.assertIsNotNone(KnowledgePlatformAPIHandler.indexer)
        self.assertIsNotNone(KnowledgePlatformAPIHandler.refactor)


if __name__ == "__main__":
    unittest.main()
