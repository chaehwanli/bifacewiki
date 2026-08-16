"""
Automated Test Suite for NFR Performance Benchmarks (NFR-PERF-01 ~ NFR-PERF-05)
"""

import os
import time
import shutil
import tempfile
import pytest

from src.storage.git_operations_adapter import GitOperationsAdapter
from src.indexer.ref_dag_indexer_engine import RefDAGIndexerEngine
from src.core.knowledge_ingestion_engine import KnowledgeIngestionEngine, KnowledgeExtractRequestDTO
from src.agent.skill_binding_middleware import SkillBindingMiddleware
from src.agent.knowledge_retrieval_skill import KnowledgeRetrievalSkill


@pytest.fixture
def bench_env():
    tmp_dir = tempfile.mkdtemp()
    yield tmp_dir
    shutil.rmtree(tmp_dir)


def test_nfr_perf_01_ingestion_latency(bench_env):
    """NFR-PERF-01: Ingestion latency must be < 3 seconds."""
    engine = KnowledgeIngestionEngine(bench_env)
    start = time.time()
    engine.extract_from_conversation(KnowledgeExtractRequestDTO(
        conversation_session_id="bench-01",
        raw_conversation_log="Benchmark test log for ingestion speed."
    ))
    elapsed = time.time() - start
    assert elapsed < 3.0, f"Ingestion latency target failed: {elapsed:.3f}s >= 3.0s"


def test_nfr_perf_02_indexer_incremental_latency(bench_env):
    """NFR-PERF-02: Ref-DAG Incremental Sync latency must be < 50ms."""
    indexer = RefDAGIndexerEngine()
    f1 = os.path.join(bench_env, "bench-node.md")
    with open(f1, 'w') as f:
        f.write("---\nid: bench-node\ntitle: Bench\ntype: concept\nstatus: production\nauthor_type: human_authored\n---\n# Bench\nText")

    start = time.time()
    indexer.reindex_incremental([f1])
    elapsed_ms = (time.time() - start) * 1000
    assert elapsed_ms < 50.0, f"Incremental sync latency target failed: {elapsed_ms:.2f}ms >= 50ms"


def test_nfr_perf_03_git_commit_latency(bench_env):
    """NFR-PERF-03: Git Commit latency must be < 500ms."""
    git_adapter = GitOperationsAdapter(bench_env)
    git_adapter._run_cmd(["init"])
    git_adapter._run_cmd(["config", "user.name", "Bench"])
    git_adapter._run_cmd(["config", "user.email", "bench@test.com"])

    f1 = os.path.join(bench_env, "test.txt")
    with open(f1, 'w') as f:
        f.write("test content")

    start = time.time()
    git_adapter.commit(["test.txt"], "bench commit", "Bench <bench@test.com>")
    elapsed = time.time() - start
    assert elapsed < 0.5, f"Git commit latency target failed: {elapsed:.3f}s >= 0.5s"


def test_nfr_perf_04_skill_binding_latency(bench_env):
    """NFR-PERF-04: One-Click Skill Binding latency must be < 200ms."""
    skill_dir = os.path.join(bench_env, ".skill", "ingestion")
    os.makedirs(skill_dir, exist_ok=True)
    with open(os.path.join(skill_dir, "SKILL.md"), 'w') as f:
        f.write("---\nname: ingestion\ndescription: test\n---\n# Test Skill Instructions")

    middleware = SkillBindingMiddleware(bench_env)
    start = time.time()
    middleware.bind_skill("sess-bench", "ingestion")
    elapsed_ms = (time.time() - start) * 1000
    assert elapsed_ms < 200.0, f"Skill binding latency target failed: {elapsed_ms:.2f}ms >= 200ms"


def test_nfr_perf_05_retrieval_latency(bench_env):
    """NFR-PERF-05: Context retrieval & injection latency must be < 500ms."""
    indexer = RefDAGIndexerEngine()
    f1 = os.path.join(bench_env, "prod-node.md")
    with open(f1, 'w') as f:
        f.write("---\nid: prod-node\ntitle: Prod Node\ntype: concept\nstatus: production\nauthor_type: human_authored\n---\n# Prod Node\nContent")

    indexer.reindex_incremental([f1])
    skill = KnowledgeRetrievalSkill(indexer)

    start = time.time()
    results = skill.knowledge_search("Prod")
    assert len(results) == 1
    ctx = skill.knowledge_retrieve("prod-node")
    injected = skill.knowledge_context_inject(ctx)
    elapsed_ms = (time.time() - start) * 1000

    assert elapsed_ms < 500.0, f"Retrieval latency target failed: {elapsed_ms:.2f}ms >= 500ms"
    assert "Prod Node" in injected
