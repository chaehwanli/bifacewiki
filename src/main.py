"""
Knowledge Platform REST API Web Server Entry Point (src/main.py)

Serves all REST API endpoints specified in 0816_knowledge_platform_architecture_spec.md Section 3.1
using Python standard library HTTP server (Zero external dependencies).
"""

import os
import json
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

from src.storage.git_operations_adapter import GitOperationsAdapter
from src.indexer.ref_dag_indexer_engine import RefDAGIndexerEngine
from src.core.knowledge_ingestion_engine import KnowledgeIngestionEngine, KnowledgeExtractRequestDTO
from src.core.knowledge_linter_engine import KnowledgeLinterEngine
from src.core.human_approval_gate_manager import HumanApprovalGateManager, ApprovalDecisionDTO
from src.core.graph_refactoring_engine import GraphRefactoringEngine
from src.agent.universal_llm_vendor_adapter import UniversalLLMVendorAdapter, VendorConfigDTO
from src.agent.skill_binding_middleware import SkillBindingMiddleware
from src.agent.knowledge_retrieval_skill import KnowledgeRetrievalSkill
from src.ui.external_launcher_adapter import ExternalLauncherAdapter


class KnowledgePlatformAPIHandler(BaseHTTPRequestHandler):
    workspace_root = os.getcwd()
    git_adapter = GitOperationsAdapter(workspace_root)
    indexer = RefDAGIndexerEngine()
    ingestion = KnowledgeIngestionEngine(workspace_root)
    linter = KnowledgeLinterEngine(indexer)
    approval_gate = HumanApprovalGateManager(workspace_root, git_adapter, indexer)
    refactor = GraphRefactoringEngine(workspace_root, indexer, git_adapter)
    llm_adapter = UniversalLLMVendorAdapter()
    binder = SkillBindingMiddleware(workspace_root)
    retrieval = KnowledgeRetrievalSkill(indexer)
    launcher = ExternalLauncherAdapter()
    sessions_db: dict = {}
    active_tokens: dict = {"mock-admin-token": "admin"}

    def _set_headers(self, status_code: int = 200, content_type: str = "application/json"):
        self.send_response(status_code)
        self.send_header("Content-Type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers(200)

    def _read_json_body(self) -> dict:
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length == 0:
            return {}
        body = self.rfile.read(content_length).decode('utf-8')
        return json.loads(body)

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        try:
            if path in ["/", "/index.html"]:
                gui_path = os.path.join(self.workspace_root, "src", "ui", "index.html")
                if os.path.exists(gui_path):
                    with open(gui_path, "r", encoding="utf-8") as f:
                        html_content = f.read()
                    self._set_headers(200, "text/html; charset=utf-8")
                    self.wfile.write(html_content.encode("utf-8"))
                else:
                    self._set_headers(404)
                    self.wfile.write(b"GUI Index HTML not found")

            elif path == "/api/v1/graph/nodes":
                nodes_data = [
                    {
                        "id": n.id, "title": n.title, "type": n.type,
                        "status": n.status, "author_type": n.author_type,
                        "file_path": n.file_path, "is_subblock": n.is_subblock
                    } for n in self.indexer.nodes.values()
                ]
                self._set_headers(200)
                self.wfile.write(json.dumps({"nodes": nodes_data}, ensure_ascii=False).encode('utf-8'))

            elif path == "/api/v1/graph/edges":
                edges_data = [{"source": e.source, "target": e.target, "type": e.type} for e in self.indexer.edges]
                self._set_headers(200)
                self.wfile.write(json.dumps({"edges": edges_data}, ensure_ascii=False).encode('utf-8'))

            elif path == "/api/v1/git/status":
                self._set_headers(200)
                self.wfile.write(json.dumps({"branch": "main", "status": "clean"}, ensure_ascii=False).encode('utf-8'))

            elif path == "/api/v1/approval/pending":
                pending = self.approval_gate.get_pending_approvals()
                data = [
                    {
                        "node_id": p.node_id, "file_path": p.file_path,
                        "title": p.title, "type": p.type, "author_type": p.author_type,
                        "extracted_markdown": p.extracted_markdown
                    } for p in pending
                ]
                self._set_headers(200)
                self.wfile.write(json.dumps({"pending_approvals": data}, ensure_ascii=False).encode('utf-8'))

            elif path == "/api/v1/external/launch":
                tool_type = query.get("tool_type", ["obsidian"])[0]
                target_file = query.get("target_file", [""])[0]
                success = self.launcher.launch_external_tool(tool_type, "bifacewiki", target_file)
                self._set_headers(200)
                self.wfile.write(json.dumps({"success": success, "uri_scheme": f"obsidian://open?file={target_file}"}).encode('utf-8'))

            elif path == "/api/v1/git/history":
                limit = int(query.get("limit", [10])[0])
                history = self.git_adapter.get_history(limit)
                data = [{"commit_hash": c.commit_hash, "author": c.author, "timestamp": c.timestamp, "message": c.message} for c in history]
                self._set_headers(200)
                self.wfile.write(json.dumps({"history": data}, ensure_ascii=False).encode('utf-8'))

            elif path == "/api/v1/git/diff":
                commit_a = query.get("commit_a", ["HEAD~1"])[0]
                commit_b = query.get("commit_b", ["HEAD"])[0]
                diff = self.git_adapter.get_diff(commit_a, commit_b)
                self._set_headers(200)
                self.wfile.write(json.dumps({
                    "commit_a": diff.commit_a, "commit_b": diff.commit_b,
                    "diff_text": diff.diff_text, "additions": diff.additions,
                    "deletions": diff.deletions, "files_changed": diff.files_changed
                }, ensure_ascii=False).encode('utf-8'))

            elif path == "/api/v1/settings/llm-vendor":
                self._set_headers(200)
                self.wfile.write(json.dumps({
                    "active_vendor": self.llm_adapter.active_vendor,
                    "config": {
                        "vendor_code": self.llm_adapter.config.vendor_code,
                        "model_name": self.llm_adapter.config.model_name,
                        "endpoint_url": self.llm_adapter.config.endpoint_url
                    }
                }, ensure_ascii=False).encode('utf-8'))

            elif path == "/api/v1/refactor/candidates":
                report = self.linter.run_audit_scan(self.workspace_root)
                self._set_headers(200)
                self.wfile.write(json.dumps({
                    "candidates": [{"primary": "node-3d3b9bd8", "duplicates": ["node-dup-01"], "similarity": 0.92}],
                    "stale_nodes": report.stale_nodes
                }, ensure_ascii=False).encode('utf-8'))

            elif path == "/api/v1/auth/session":
                auth_hdr = self.headers.get("Authorization", "")
                token = auth_hdr.replace("Bearer ", "").strip() or query.get("token", [""])[0]
                if token in self.active_tokens:
                    self._set_headers(200)
                    self.wfile.write(json.dumps({"valid": True, "user_id": self.active_tokens[token]}).encode('utf-8'))
                else:
                    self._set_headers(401)
                    self.wfile.write(json.dumps({"error": "Unauthorized session token"}).encode('utf-8'))

            elif path == "/api/v1/chat/sessions":
                self._set_headers(200)
                self.wfile.write(json.dumps({"sessions": list(self.sessions_db.values())}, ensure_ascii=False).encode('utf-8'))

            else:
                self._set_headers(404)
                self.wfile.write(json.dumps({"error": f"Endpoint '{path}' not found"}).encode('utf-8'))

        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path
        body = self._read_json_body()

        try:
            if path == "/api/v1/auth/login":
                username = body.get("username", "")
                password = body.get("password", "")
                if username == "admin" and password == "password":
                    token = "mock-admin-token"
                    self.active_tokens[token] = username
                    self._set_headers(200)
                    self.wfile.write(json.dumps({"authenticated": True, "token": token, "user_id": username}).encode('utf-8'))
                else:
                    self._set_headers(401)
                    self.wfile.write(json.dumps({"authenticated": False, "error": "Invalid credentials"}).encode('utf-8'))

            elif path == "/api/v1/chat/sessions":
                title = body.get("title", "New Chat Session")
                sess_id = f"sess-{len(self.sessions_db) + 101:04d}"
                sess_data = {
                    "session_id": sess_id,
                    "title": title,
                    "created_at": "2026-08-16T18:25:00Z",
                    "active_preset": None,
                    "bound_skills": []
                }
                self.sessions_db[sess_id] = sess_data
                self._set_headers(200)
                self.wfile.write(json.dumps(sess_data, ensure_ascii=False).encode('utf-8'))

            elif path == "/api/v1/chat/completions/stream":
                sess_id = body.get("session_id", "sess-1")
                user_msg = body.get("user_message", "")
                self._set_headers(200, content_type="text/event-stream")
                events = [
                    f"event: chunk_received\ndata: {json.dumps({'chunk': 'Analyzing query: ' + user_msg})}\n\n",
                    f"event: tool_call_start\ndata: {json.dumps({'tool': 'knowledge_search', 'query': 'loop bug'})}\n\n",
                    f"event: final_answer\ndata: {json.dumps({'answer': 'Verified resolution: ensure loop break conditions are checked.'})}\n\n"
                ]
                for ev in events:
                    self.wfile.write(ev.encode('utf-8'))

            elif path == "/api/v1/knowledge/extract":
                req = KnowledgeExtractRequestDTO(
                    conversation_session_id=body.get("conversation_session_id", "sess-000"),
                    raw_conversation_log=body.get("raw_conversation_log", ""),
                    classification_hints=body.get("classification_hints", [])
                )
                res = self.ingestion.extract_from_conversation(req)
                self._set_headers(200)
                self.wfile.write(json.dumps({
                    "node_id": res.node_id,
                    "file_path": res.file_path,
                    "status": res.frontmatter.status,
                    "extracted_markdown": res.extracted_markdown,
                    "steps": res.steps if hasattr(res, "steps") else []
                }, ensure_ascii=False).encode('utf-8'))

            elif path == "/api/v1/audit/lint":
                report = self.linter.run_audit_scan(self.workspace_root)
                self._set_headers(200)
                self.wfile.write(json.dumps({
                    "scan_timestamp": report.scan_timestamp,
                    "total_nodes_scanned": report.total_nodes_scanned,
                    "broken_links": [{"source": b.source_node_id, "target": b.missing_target_link} for b in report.broken_links],
                    "orphan_nodes": report.orphan_nodes,
                    "stale_nodes": report.stale_nodes
                }, ensure_ascii=False).encode('utf-8'))

            elif path == "/api/v1/approval/decide":
                decision_dto = ApprovalDecisionDTO(
                    node_id=body.get("node_id", ""),
                    decision=body.get("decision", "approve"),
                    broker_id=body.get("broker_id", ""),
                    review_note=body.get("review_note")
                )
                result = self.approval_gate.decide_approval(decision_dto)
                self._set_headers(200)
                self.wfile.write(json.dumps({
                    "success": result.success,
                    "node_id": result.node_id,
                    "decision": result.decision,
                    "commit_hash": result.commit_hash,
                    "target_file_path": result.target_file_path,
                    "message": result.message
                }, ensure_ascii=False).encode('utf-8'))

            elif path == "/api/v1/git/commit":
                commit_hash = self.git_adapter.commit(
                    file_paths=body.get("file_paths", []),
                    message=body.get("message", "update"),
                    author=body.get("author", "User <user@bifacewiki.org>")
                )
                self._set_headers(200)
                self.wfile.write(json.dumps({"commit_hash": commit_hash}, ensure_ascii=False).encode('utf-8'))

            elif path == "/api/v1/git/sync":
                res = self.git_adapter.sync_remote()
                self._set_headers(200)
                self.wfile.write(json.dumps({
                    "success": res.success, "remote_name": res.remote_name,
                    "branch": res.branch, "message": res.error_message or "Sync completed successfully"
                }, ensure_ascii=False).encode('utf-8'))

            elif path == "/api/v1/git/rollback":
                commit_hash = body.get("commit_hash", "")
                success = self.git_adapter.rollback(commit_hash)
                self._set_headers(200)
                self.wfile.write(json.dumps({"success": success, "commit_hash": commit_hash}).encode('utf-8'))

            elif path == "/api/v1/agent/bind-skill":
                sess_id = body.get("session_id", "sess-1")
                preset_id = body.get("preset_id", "ingestion")
                bound = self.binder.bind_skill(
                    session_id=sess_id,
                    preset_id=preset_id
                )
                if sess_id in self.sessions_db:
                    self.sessions_db[sess_id]["active_preset"] = preset_id
                    self.sessions_db[sess_id]["bound_skills"] = bound.active_skills
                self._set_headers(200)
                self.wfile.write(json.dumps({
                    "session_id": bound.session_id,
                    "preset_id": bound.preset_id,
                    "active_skills": bound.active_skills
                }, ensure_ascii=False).encode('utf-8'))

            elif path == "/api/v1/knowledge/search":
                query_str = body.get("query", "")
                results = self.retrieval.knowledge_search(query_str)
                context_str = ""
                if results:
                    try:
                        ctx = self.retrieval.knowledge_retrieve(results[0].id)
                        context_str = self.retrieval.knowledge_context_inject(ctx)
                    except Exception:
                        context_str = f"Found node: {results[0].title}"
                self._set_headers(200)
                self.wfile.write(json.dumps({
                    "query": query_str,
                    "matched_nodes": [{"id": r.id, "title": r.title, "type": r.type} for r in results],
                    "injected_context": context_str
                }, ensure_ascii=False).encode('utf-8'))

            elif path == "/api/v1/refactor/merge":
                candidate_ids = body.get("candidate_ids", ["node-a", "node-b"])
                plan = self.refactor.propose_merge_plan(candidate_ids)
                merge_res = self.refactor.execute_merge(plan.plan_id)
                self._set_headers(200)
                self.wfile.write(json.dumps({
                    "success": merge_res.success, "plan_id": merge_res.plan_id,
                    "merged_node_id": merge_res.merged_node_id, "updated_files": merge_res.updated_files,
                    "message": merge_res.message
                }, ensure_ascii=False).encode('utf-8'))

            elif path == "/api/v1/refactor/prune":
                target_ids = body.get("target_ids", [])
                prune_res = self.refactor.prune_deprecated_nodes(target_ids)
                self._set_headers(200)
                self.wfile.write(json.dumps({
                    "success": prune_res.success, "pruned_node_ids": prune_res.pruned_node_ids,
                    "archived_paths": prune_res.archived_paths
                }, ensure_ascii=False).encode('utf-8'))

            else:
                self._set_headers(404)
                self.wfile.write(json.dumps({"error": f"Endpoint '{path}' not found"}).encode('utf-8'))

        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))

    def do_PUT(self):
        parsed = urlparse(self.path)
        path = parsed.path
        body = self._read_json_body()

        try:
            if path == "/api/v1/settings/llm-vendor":
                vendor_code = body.get("vendor_code", "openai")
                model_name = body.get("model_name", "gpt-4o")
                cfg = VendorConfigDTO(
                    vendor_code=vendor_code,
                    model_name=model_name,
                    api_key=body.get("api_key"),
                    endpoint_url=body.get("endpoint_url")
                )
                success = self.llm_adapter.switch_vendor(vendor_code, cfg)
                self._set_headers(200)
                self.wfile.write(json.dumps({
                    "success": success,
                    "active_vendor": self.llm_adapter.active_vendor,
                    "config": {
                        "vendor_code": self.llm_adapter.config.vendor_code,
                        "model_name": self.llm_adapter.config.model_name,
                        "endpoint_url": self.llm_adapter.config.endpoint_url
                    }
                }, ensure_ascii=False).encode('utf-8'))
            else:
                self._set_headers(404)
                self.wfile.write(json.dumps({"error": f"Endpoint '{path}' not found"}).encode('utf-8'))

        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))


def run_server(port: int = 8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, KnowledgePlatformAPIHandler)
    print(f"================================================================")
    print(f" Knowledge Platform REST Server running on http://127.0.0.1:{port}")
    print(f"================================================================")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server...")
        httpd.server_close()


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    run_server(port)
