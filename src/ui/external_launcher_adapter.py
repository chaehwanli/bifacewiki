"""
External Launcher Adapter (DSGN-LAUNCHER-PROTOCOL)

Triggers OS URI schemes (e.g. obsidian://open?vault=...&file=...)
to launch external PKM tools (Obsidian, Logseq) directly from the Web UI (UC-011, NFR-COMP-01).
"""

import urllib.parse
import subprocess
import sys


class ExternalLauncherAdapter:
    def __init__(self, default_vault_name: str = "bifacewiki"):
        self.default_vault_name = default_vault_name

    def construct_obsidian_uri(self, vault_name: str, target_file: str) -> str:
        """
        Constructs obsidian:// URI scheme string.
        """
        encoded_vault = urllib.parse.quote(vault_name)
        encoded_file = urllib.parse.quote(target_file)
        return f"obsidian://open?vault={encoded_vault}&file={encoded_file}"

    def launch_external_tool(self, tool_type: str, vault_path: str, target_file: str) -> bool:
        """
        Executes OS URI scheme command to open external visualizer.
        """
        if tool_type.lower() == "obsidian":
            uri = self.construct_obsidian_uri(vault_path or self.default_vault_name, target_file)
        else:
            raise ValueError(f"Unsupported external tool type '{tool_type}'.")

        try:
            if sys.platform == "darwin":
                subprocess.run(["open", uri], check=True)
            elif sys.platform.startswith("linux"):
                subprocess.run(["xdg-open", uri], check=True)
            elif sys.platform == "win32":
                subprocess.run(["cmd", "/c", "start", uri], check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            print(f"[Warning] Failed to launch OS URI scheme '{uri}': {e}")
            return False
