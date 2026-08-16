"""
Skill Binding Middleware (DSGN-AGENT-BINDER)

Loads skill definitions from .skill/ and .agent/skills/ directories,
and binds System Prompts & Function Calling Tool Schemas to active LLM sessions.
"""

import os
import re
import time
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass
class SkillDefinitionDTO:
    skill_name: str
    description: str
    system_prompt_template: str
    tools: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class BoundSessionDTO:
    session_id: str
    preset_id: str
    active_skills: List[str]
    system_prompt: str
    bound_tools: List[Dict[str, Any]]


class SkillBindingMiddleware:
    def __init__(self, workspace_root: str):
        self.workspace_root = os.path.abspath(workspace_root)
        self.skills_dir = os.path.join(self.workspace_root, ".skill")

    def load_skill_definition(self, skill_path: str) -> SkillDefinitionDTO:
        """
        Loads skill YAML Frontmatter and markdown body instructions.
        """
        full_path = os.path.join(self.skills_dir, skill_path, "SKILL.md") if not os.path.isabs(skill_path) else skill_path
        if not os.path.exists(full_path):
            raise FileNotFoundError(f"Skill definition file '{full_path}' not found.")

        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()

        match = re.search(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        meta = {}
        body = content
        if match:
            for line in match.group(1).splitlines():
                if ':' in line:
                    k, v = line.split(':', 1)
                    meta[k.strip()] = v.strip().strip('"\'')
            body = content[match.end():]

        name = meta.get('name', os.path.basename(os.path.dirname(full_path)))
        desc = meta.get('description', '')

        # Construct standard tools if applicable
        tools = []
        if name in ["agent_binder", "indexer_dag"]:
            tools = [
                {
                    "name": "knowledge_search",
                    "description": "Searches Ref-DAG nodes for query string",
                    "parameters": {"type": "object", "properties": {"query": {"type": "string"}}}
                },
                {
                    "name": "knowledge_retrieve",
                    "description": "Retrieves node details and content",
                    "parameters": {"type": "object", "properties": {"node_id": {"type": "string"}}}
                }
            ]

        return SkillDefinitionDTO(
            skill_name=name,
            description=desc,
            system_prompt_template=body,
            tools=tools
        )

    def bind_skill(self, session_id: str, preset_id: str) -> BoundSessionDTO:
        """
        Binds preset skills to LLM session dynamically.
        Latency target: < 200ms (NFR-PERF-04).
        """
        start_time = time.time()

        preset_map = {
            "qa_ingestion": "ingestion",
            "linter_audit": "linter_engine",
            "refactor_merge": "refactor_engine",
            "knowledge_retrieval": "agent_binder"
        }
        target_skill = preset_map.get(preset_id, preset_id)
        skill_path = os.path.join(self.skills_dir, target_skill, "SKILL.md")
        if not os.path.exists(skill_path):
            target_skill = "ingestion"

        skill_def = self.load_skill_definition(target_skill)

        bound_session = BoundSessionDTO(
            session_id=session_id,
            preset_id=preset_id,
            active_skills=[skill_def.skill_name],
            system_prompt=f"System Role Instructions for {skill_def.skill_name}:\n{skill_def.system_prompt_template}",
            bound_tools=skill_def.tools
        )

        elapsed = (time.time() - start_time) * 1000
        if elapsed > 200:
            print(f"[Warning] One-click skill binding latency target exceeded: {elapsed:.2f}ms")

        return bound_session
