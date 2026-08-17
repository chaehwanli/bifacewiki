---
name: antigravity_cli
description: Skill for Google Antigravity CLI installation, login/auth verification, real LLM invocation integration, debugging, and network error/retry handling. Activate when implementing, debugging, or configuring Google Antigravity CLI vendor integration.
---

# Google Antigravity CLI Integration & Operation Skill

## Overview
Instructions and operational guidelines for integrating, executing, and troubleshooting **Google Antigravity CLI (`antigravity`)** as the primary real LLM vendor engine in `UniversalLLMVendorAdapter` (`DSGN-LLM-ADAPTER`).

---

## 1. Installation & Environment Setup (설치 및 환경 구성)

### 1.1 Binary & Package Verification
- **CLI Executable Check**:
  ```bash
  which antigravity
  ```
  Ensure binary exists at `/usr/local/bin/antigravity` or within `$PATH`.
- **Python SDK Installation Check**:
  ```bash
  pip show google-antigravity
  ```
  Verify `google-antigravity` (v0.1.9+) is installed in the active Python virtual environment.

### 1.2 Authentication Modes (로그인 및 인증)
Google Antigravity CLI support two primary authentication methods:

1. **API Key Mode (Recommended for Service Integration)**:
   - Set environment variable:
     ```bash
     export GEMINI_API_KEY="AIzaSy..."
     ```
   - Pass explicitly via `VendorConfigDTO(api_key="...")`.
   - Key generation link: `https://aistudio.google.com/app/api-keys`

2. **Google Cloud ADC (Application Default Credentials)**:
   - Run interactive CLI login:
     ```bash
     gcloud auth application-default login
     ```
   - Verify credentials file at `~/.config/gcloud/application_default_credentials.json`.

3. **Interactive Antigravity CLI Auth**:
   - Run CLI auth command if available:
     ```bash
     antigravity auth login
     ```

---

## 2. Real Invocation & Integration Pattern (실제 LLM 연동 구현)

### 2.1 Vendor Adapter Integration Pattern
When `active_vendor == "antigravity"`, `UniversalLLMVendorAdapter` executes real inference requests:

```python
import os
import subprocess
import shutil
import google.antigravity as agy
from src.agent.universal_llm_vendor_adapter import LLMInvokeRequestDTO, LLMInvokeResponseDTO

def invoke_antigravity_cli(request: LLMInvokeRequestDTO, config) -> LLMInvokeResponseDTO:
    # 1. API Key & Auth Retrieval
    api_key = config.api_key or os.environ.get("GEMINI_API_KEY")
    
    # 2. SDK Agent Construction
    agent_cfg = agy.LocalAgentConfig(
        api_key=api_key if api_key else None,
        model_name=config.model_name or "antigravity-agent-v1"
    )
    
    # 3. Invocation with Error Resilience
    ...
```

### 2.2 Mock Notice Requirement for Non-Supported Vendors
- Live execution is **strictly restricted** to `antigravity`.
- All other vendor codes (`openai`, `gemini`, `claude`, `ollama`) MUST output clear `[MOCK - Vendor (Not Connected)]` status messages and set `is_mock = True`.

---

## 3. Network Error Handling & Retry Policies (네트워크 에러 처리 및 재시도)

### 3.1 Error Taxonomy & Recovery Matrix
| Error Type | Trigger Cause | Recovery Action / Strategy |
| :--- | :--- | :--- |
| **`TimeoutError` / `subprocess.TimeoutExpired`** | Gateway or endpoint non-responsive (>30s) | Exponential backoff retry (Max 2 retries, initial delay 1.0s) |
| **`ConnectionRefusedError` / Socket Error** | Local proxy or daemon unreachable | Check `127.0.0.1` status, retry after 2.0s delay |
| **`429 Too Many Requests` (Rate Limit)** | API Quota exceeded | Read `Retry-After` header or apply Jitter Backoff ($1s \rightarrow 2s \rightarrow 4s$) |
| **`AuthError` / `401 Unauthorized`** | Missing or expired `GEMINI_API_KEY` | Log diagnostic error: `"GEMINI_API_KEY missing or invalid"`, abort retry |
| **`CLI Executable Missing`** | `antigravity` binary not found in `$PATH` | Fall back to `google.antigravity` Python SDK execution |

### 3.2 Retry Implementation Snippet
```python
max_retries = 2
for attempt in range(max_retries + 1):
    try:
        # Perform CLI or SDK invocation
        result = execute_antigravity(prompt=request.prompt)
        return result
    except (TimeoutError, ConnectionError) as e:
        if attempt == max_retries:
            return LLMInvokeResponseDTO(
                vendor_code="antigravity",
                content=f"[Google Antigravity CLI Error] Network failure after retries: {str(e)}",
                is_mock=False
            )
        time.sleep(1.0 * (attempt + 1))
```

---

## 4. Debugging & Diagnostic Operations (디버깅 및 운영)

### 4.1 CLI Debug Logs
- Enable verbose logging when executing CLI commands:
  ```bash
  antigravity --verbose --log-level=DEBUG
  ```
- Inspect Electron & Language Server log files:
  - Language Server Log: `~/.config/Antigravity/logs/language_server.log`
  - Electron Main Log: `~/.config/Antigravity/logs/main.log`

### 4.2 Health Check Diagnostic Function
Use the following snippet to verify CLI readiness:
```python
def check_antigravity_cli_health() -> Dict[str, Any]:
    cli_exists = shutil.which("antigravity") is not None
    has_api_key = bool(os.environ.get("GEMINI_API_KEY"))
    sdk_installed = True
    try:
        import google.antigravity
    except ImportError:
        sdk_installed = False
        
    return {
        "cli_binary_found": cli_exists,
        "sdk_installed": sdk_installed,
        "api_key_configured": has_api_key,
        "ready": (cli_exists or sdk_installed)
    }
```
