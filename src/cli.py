"""
Knowledge Platform Command Line Interface (CLI) Entry Point (src/cli.py)

Allows command-line terminal execution for platform features:
serve, ingest, audit, pending, approve, search, and graph.
"""

import sys
import os
import argparse
import json

from src.storage.git_operations_adapter import GitOperationsAdapter
from src.indexer.ref_dag_indexer_engine import RefDAGIndexerEngine
from src.core.knowledge_ingestion_engine import KnowledgeIngestionEngine, KnowledgeExtractRequestDTO
from src.core.knowledge_linter_engine import KnowledgeLinterEngine
from src.core.human_approval_gate_manager import HumanApprovalGateManager, ApprovalDecisionDTO
from src.agent.knowledge_retrieval_skill import KnowledgeRetrievalSkill
from src.main import run_server


def main():
    parser = argparse.ArgumentParser(description="Bifacewiki Knowledge Platform CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # Command: serve
    serve_parser = subparsers.add_parser("serve", help="Start REST API Web Server")
    serve_parser.add_argument("--port", type=int, default=8000, help="Port to run HTTP server on (default: 8000)")

    # Command: ingest
    ingest_parser = subparsers.add_parser("ingest", help="Ingest Q&A conversation into Atomic Draft Node")
    ingest_parser.add_argument("--log", type=str, required=True, help="Raw conversation text log")
    ingest_parser.add_argument("--session", type=str, default="cli-sess", help="Session ID")

    # Command: audit
    subparsers.add_parser("audit", help="Run 24/7 static Linter audit scan across markdown store")

    # Command: pending
    subparsers.add_parser("pending", help="List draft nodes awaiting Human Broker approval")

    # Command: approve
    approve_parser = subparsers.add_parser("approve", help="Approve draft node and promote to production (Human Broker)")
    approve_parser.add_argument("--node", type=str, required=True, help="Draft node ID to approve")
    approve_parser.add_argument("--broker", type=str, required=True, help="Human Broker ID (AI agent bot IDs blocked NFR-SEC-01)")

    # Command: search
    search_parser = subparsers.add_parser("search", help="Search production knowledge graph nodes")
    search_parser.add_argument("--query", type=str, required=True, help="Search query string")

    # Command: graph
    subparsers.add_parser("graph", help="Display summary of current Ref-DAG nodes and edges")

    args = parser.parse_args()

    workspace_root = os.getcwd()
    git_adapter = GitOperationsAdapter(workspace_root)
    indexer = RefDAGIndexerEngine()
    ingestion = KnowledgeIngestionEngine(workspace_root)
    linter = KnowledgeLinterEngine(indexer)
    approval_gate = HumanApprovalGateManager(workspace_root, git_adapter, indexer)
    retrieval = KnowledgeRetrievalSkill(indexer)

    if args.command == "serve":
        run_server(port=args.port)

    elif args.command == "ingest":
        req = KnowledgeExtractRequestDTO(conversation_session_id=args.session, raw_conversation_log=args.log)
        res = ingestion.extract_from_conversation(req)
        print(f"[Ingest Success]")
        print(f"  Node ID   : {res.node_id}")
        print(f"  File Path : {res.file_path}")
        print(f"  Status    : {res.frontmatter.status}")
        print(f"  Type      : {res.frontmatter.type}")

    elif args.command == "audit":
        # First index existing files
        all_md = []
        for root, _, files in os.walk(workspace_root):
            for f in files:
                if f.endswith('.md'):
                    all_md.append(os.path.join(root, f))
        indexer.reindex_incremental(all_md)

        report = linter.run_audit_scan(workspace_root)
        print(f"[Lint Audit Report] Time: {report.scan_timestamp}")
        print(f"  Total Scanned : {report.total_nodes_scanned}")
        print(f"  Broken Links  : {len(report.broken_links)}")
        print(f"  Orphan Nodes  : {len(report.orphan_nodes)}")
        print(f"  Stale Nodes   : {len(report.stale_nodes)}")

    elif args.command == "pending":
        pending = approval_gate.get_pending_approvals()
        print(f"[Pending Review Queue] Count: {len(pending)}")
        for p in pending:
            print(f"  - [{p.node_id}] {p.title} (type: {p.type}, author: {p.author_type})")

    elif args.command == "approve":
        try:
            res = approval_gate.decide_approval(ApprovalDecisionDTO(
                node_id=args.node,
                decision="approve",
                broker_id=args.broker
            ))
            print(f"[Approval Success] Node '{res.node_id}' promoted to '{res.target_file_path}' (Commit: {res.commit_hash})")
        except PermissionError as pe:
            print(f"[Security Block NFR-SEC-01] {pe}")

    elif args.command == "search":
        # Index production files
        prod_dir = os.path.join(workspace_root, "knowledge")
        if os.path.exists(prod_dir):
            indexer.reindex_incremental([os.path.join(prod_dir, f) for f in os.listdir(prod_dir) if f.endswith('.md')])
        results = retrieval.knowledge_search(args.query)
        print(f"[Search Results for '{args.query}'] Count: {len(results)}")
        for r in results:
            print(f"  - [{r.id}] {r.title} ({r.type})")

    elif args.command == "graph":
        print(f"[Ref-DAG Graph Summary]")
        print(f"  Total Nodes: {len(indexer.nodes)}")
        print(f"  Total Edges: {len(indexer.edges)}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
