---
name: presentation_ui
description: Presentation Layer skill for building Git Management Dashboard, Visual Line-by-Line Diff Viewer, Approval Gate UI Widget, and External Launcher Adapter for Obsidian OS URI schemes (UC-004, UC-011). Activate when building React Web UI or external protocol launchers.
---

# Presentation UI & External Launcher Skill (`DSGN-UI-DASHBOARD`, `DSGN-LAUNCHER-PROTOCOL`)

## Overview
Instructions and domain rules for building the **Presentation Layer** web UI components and external launcher adapters.

## Core Responsibilities & Specifications
1. **Git Management Dashboard (`DSGN-UI-DASHBOARD`, `UC-004`)**:
   - Provide visual Git repository status (Staged/Unstaged), commit timeline, and sync progress bars without CLI dependence.
   - Render Visual Line-by-Line Diff Viewer comparing commits and draft states.
   - Provide one-click commit rollback interface.
2. **Human Approval Gate Widget (`DSGN-APPROVAL-GATE`)**:
   - Render draft review queue cards with side-by-side markdown comparison and Linter audit results.
   - Provide explicit [Approve & Merge], [Reject], and [Request Revision] buttons.
3. **One-Click Skill Binding UI (`DSGN-AGENT-BINDER`)**:
   - Render preset skill binder cards for quick session activation.
4. **External Launcher Adapter (`DSGN-LAUNCHER-PROTOCOL`, `UC-011`)**:
   - Trigger OS URI schemes (`obsidian://open?vault=...&file=...`) to open vault nodes directly in Obsidian/Logseq (`NFR-COMP-01`).

## Key UI Components & REST Endpoints
- **UI Component**: `render_status_widget(repo_path: str) -> JSX.Element`
- **UI Component**: `render_timeline_widget(history: List[CommitDTO]) -> JSX.Element`
- **UI Component**: `render_diff_modal(commit_hash_a: str, commit_hash_b: str) -> JSX.Element`
- **Method**: `launch_external_tool(tool_type: str, vault_path: str, target_file: str) -> bool`
- **REST Endpoints**: `GET /api/v1/git/status`, `GET /api/v1/git/history`, `GET /api/v1/external/launch`

## 🚨 Strict Design & Usability Rules
- **Non-Technical Usability**: Web UI must allow complete Git version management and approval workflow without requiring CLI terminal execution.
- **Visual Clarity**: Clear badge indicators for node status (`draft`, `review_pending`, `production`, `deprecated`).
