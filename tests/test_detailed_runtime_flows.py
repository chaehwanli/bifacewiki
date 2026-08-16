"""
Detailed Runtime Flows Integration & Unit Tests (tests/test_detailed_runtime_flows.py)

Tests Auth & Connection, Chat Session Management, Streaming & Tool SSE, and Ingestion Step Progress
according to .plan/0816_detailed_flow_tdd_task_plan.md.
"""

import os
import json
import time
import unittest
from io import BytesIO
from http.server import BaseHTTPRequestHandler

from src.main import KnowledgePlatformAPIHandler
from src.core.knowledge_ingestion_engine import KnowledgeIngestionEngine, KnowledgeExtractRequestDTO


class MockRequest:
    def __init__(self, body_bytes: bytes, headers: dict = None):
        self.body_bytes = body_bytes
        self.headers = headers or {'Content-Length': str(len(body_bytes))}

    def makefile(self, *args, **kwargs):
        return BytesIO(self.body_bytes)


class DummySocket:
    def __init__(self):
        self.output = BytesIO()

    def sendall(self, data):
        self.output.write(data)

    def get_output(self) -> str:
        return self.output.getvalue().decode('utf-8')


def invoke_handler(method: str, path: str, body: dict = None, headers: dict = None):
    body_bytes = json.dumps(body).encode('utf-8') if body is not None else b""
    hdr_dict = {'Content-Length': str(len(body_bytes))}
    if headers:
        hdr_dict.update(headers)
    
    sock = DummySocket()
    handler = KnowledgePlatformAPIHandler.__new__(KnowledgePlatformAPIHandler)
    handler.rfile = BytesIO(body_bytes)
    handler.wfile = sock.output
    handler.headers = hdr_dict
    handler.path = path
    handler.command = method
    handler.requestline = f"{method} {path} HTTP/1.1"
    handler.request_version = "HTTP/1.1"
    handler.protocol_version = "HTTP/1.1"
    handler.close_connection = True
    handler.client_address = ('127.0.0.1', 12345)

    # Route execution
    if method == 'GET':
        handler.do_GET()
    elif method == 'POST':
        handler.do_POST()
    elif method == 'PUT':
        handler.do_PUT()

    raw_response = sock.get_output()
    # Separate headers and body
    parts = raw_response.split('\r\n\r\n', 1)
    header_part = parts[0]
    body_part = parts[1] if len(parts) > 1 else ""

    # Parse status code
    first_line = header_part.split('\r\n')[0]
    status_code = int(first_line.split(' ')[1])

    return status_code, header_part, body_part


class TestAuthAndConnectionFlow(unittest.TestCase):
    def test_auth_login_success(self):
        """Phase 1: Test POST /api/v1/auth/login with valid credentials."""
        status_code, headers, body_str = invoke_handler(
            'POST', '/api/v1/auth/login',
            body={"username": "admin", "password": "password"}
        )
        self.assertEqual(status_code, 200)
        res = json.loads(body_str)
        self.assertTrue(res.get("authenticated"))
        self.assertIsNotNone(res.get("token"))
        self.assertEqual(res.get("user_id"), "admin")

    def test_auth_login_invalid_credentials(self):
        """Phase 1: Test POST /api/v1/auth/login with invalid password."""
        status_code, headers, body_str = invoke_handler(
            'POST', '/api/v1/auth/login',
            body={"username": "admin", "password": "wrong_password"}
        )
        self.assertEqual(status_code, 401)
        res = json.loads(body_str)
        self.assertIn("error", res)

    def test_auth_session_validation(self):
        """Phase 1: Test GET /api/v1/auth/session with valid token."""
        status_code, headers, body_str = invoke_handler(
            'GET', '/api/v1/auth/session',
            headers={"Authorization": "Bearer mock-admin-token"}
        )
        self.assertEqual(status_code, 200)
        res = json.loads(body_str)
        self.assertTrue(res.get("valid"))
        self.assertEqual(res.get("user_id"), "admin")


class TestChatSessionAndPresetFlow(unittest.TestCase):
    def test_create_chat_session(self):
        """Phase 2: Test POST /api/v1/chat/sessions creating a new session."""
        status_code, headers, body_str = invoke_handler(
            'POST', '/api/v1/chat/sessions',
            body={"title": "Loop Bug Investigation"}
        )
        self.assertEqual(status_code, 200)
        res = json.loads(body_str)
        self.assertIn("session_id", res)
        self.assertEqual(res.get("title"), "Loop Bug Investigation")

    def test_list_chat_sessions(self):
        """Phase 2: Test GET /api/v1/chat/sessions returning session list."""
        status_code, headers, body_str = invoke_handler('GET', '/api/v1/chat/sessions')
        self.assertEqual(status_code, 200)
        res = json.loads(body_str)
        self.assertIn("sessions", res)
        self.assertIsInstance(res["sessions"], list)

    def test_bind_preset_to_chat_session_latency(self):
        """Phase 2: Test POST /api/v1/agent/bind-skill completing in < 200ms (NFR-PERF-04)."""
        start_time = time.time()
        status_code, headers, body_str = invoke_handler(
            'POST', '/api/v1/agent/bind-skill',
            body={"session_id": "sess-9901", "preset_id": "qa_ingestion"}
        )
        elapsed_ms = (time.time() - start_time) * 1000.0

        self.assertEqual(status_code, 200)
        res = json.loads(body_str)
        self.assertEqual(res.get("session_id"), "sess-9901")
        self.assertEqual(res.get("preset_id"), "qa_ingestion")
        self.assertLess(elapsed_ms, 200.0, "Skill binding latency must be < 200ms (NFR-PERF-04)")


class TestTokenStreamingAndToolCallFlow(unittest.TestCase):
    def test_chat_completion_stream_chunks(self):
        """Phase 3: Test POST /api/v1/chat/completions/stream returning SSE stream with events."""
        status_code, headers, body_str = invoke_handler(
            'POST', '/api/v1/chat/completions/stream',
            body={"session_id": "sess-9901", "user_message": "How to fix loop bug?"}
        )
        self.assertEqual(status_code, 200)
        self.assertIn("Content-Type: text/event-stream", headers)
        self.assertIn("event: chunk_received", body_str)
        self.assertIn("event: tool_call_start", body_str)
        self.assertIn("event: final_answer", body_str)


class TestIngestionStepProgressUXFlow(unittest.TestCase):
    def test_knowledge_extract_progress_steps(self):
        """Phase 4: Test POST /api/v1/knowledge/extract returning 3-step progress metadata."""
        status_code, headers, body_str = invoke_handler(
            'POST', '/api/v1/knowledge/extract',
            body={
                "conversation_session_id": "sess-101",
                "raw_conversation_log": "Q: What caused infinite loop?\nA: Using while True without break condition."
            }
        )
        self.assertEqual(status_code, 200)
        res = json.loads(body_str)
        self.assertIn("node_id", res)
        self.assertEqual(res.get("status"), "draft")
        self.assertIn("steps", res)
        self.assertEqual(len(res["steps"]), 3)
        self.assertEqual(res["steps"][0]["step"], 1)
        self.assertEqual(res["steps"][1]["step"], 2)
        self.assertEqual(res["steps"][2]["step"], 3)


if __name__ == '__main__':
    unittest.main()
