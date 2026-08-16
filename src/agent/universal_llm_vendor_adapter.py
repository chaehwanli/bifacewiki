"""
Universal LLM Vendor Adapter (DSGN-LLM-ADAPTER)

Abstracts OpenAI GPT, Google Gemini, Anthropic Claude, and Local Ollama providers.
Includes Localhost Proxy Sandbox (NFR-SEC-03) for local Ollama mode to prevent external network routing.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass
class VendorConfigDTO:
    vendor_code: str  # openai, gemini, claude, ollama
    api_key: Optional[str] = None
    endpoint_url: Optional[str] = None
    model_name: str = "gpt-4o"


@dataclass
class LLMInvokeRequestDTO:
    prompt: str
    system_prompt: Optional[str] = None
    bound_tools: List[Dict[str, Any]] = field(default_factory=list)
    temperature: float = 0.7


@dataclass
class LLMInvokeResponseDTO:
    vendor_code: str
    content: str
    tool_calls: List[Dict[str, Any]] = field(default_factory=list)
    usage_tokens: int = 0


class UniversalLLMVendorAdapter:
    def __init__(self, initial_vendor: str = "openai", config: Optional[VendorConfigDTO] = None):
        self.active_vendor = initial_vendor
        self.config = config or VendorConfigDTO(vendor_code=initial_vendor)
        self._apply_security_sandbox()

    def _apply_security_sandbox(self):
        """
        Enforces NFR-SEC-03: Localhost Proxy Boundary for local Ollama mode.
        """
        if self.active_vendor == "ollama":
            self.config.endpoint_url = "http://127.0.0.1:11434"

    def switch_vendor(self, vendor_code: str, config: VendorConfigDTO) -> bool:
        """
        Switches active LLM provider.
        """
        if vendor_code not in ["openai", "gemini", "claude", "ollama"]:
            raise ValueError(f"Unsupported LLM vendor code '{vendor_code}'.")

        self.active_vendor = vendor_code
        self.config = config
        self._apply_security_sandbox()
        return True

    def invoke(self, request: LLMInvokeRequestDTO) -> LLMInvokeResponseDTO:
        """
        Invokes model via standardized vendor interface.
        """
        # Mock responses based on vendor and request
        if "knowledge_search" in str(request.bound_tools):
            return LLMInvokeResponseDTO(
                vendor_code=self.active_vendor,
                content="",
                tool_calls=[{
                    "name": "knowledge_search",
                    "arguments": {"query": request.prompt}
                }],
                usage_tokens=120
            )

        return LLMInvokeResponseDTO(
            vendor_code=self.active_vendor,
            content=f"[{self.active_vendor.upper()} Response] Processed query: {request.prompt}",
            tool_calls=[],
            usage_tokens=85
        )
