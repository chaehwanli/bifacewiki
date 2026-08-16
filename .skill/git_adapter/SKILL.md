---
name: git_adapter
description: Git Operations Adapter skill for executing low-level file-based Git operations (commit, diff, history, rollback, push/pull), managing branch transitions, and securing SSH/Token credentials via OS Secure Keychain. Activate when implementing DSGN-GIT-ADAPTER or executing Git operations.
---

# Git Operations Adapter Skill (`DSGN-GIT-ADAPTER`)

## Overview
Instructions and domain rules for implementing and operating the **Git Operations Adapter** (`DSGN-GIT-ADAPTER`).

## Core Responsibilities & Specifications
1. **File-based Version Control (`UC-003`, `UC-004`)**:
   - Provide Libgit2 / Git CLI wrapper operations (`commit`, `get_diff`, `get_history`, `rollback`, `sync_remote`).
   - Execute atomic commits for knowledge file additions, promotions, and updates.
   - Support line-by-line visual diff comparison and commit history timelines.
2. **Branch & Directory Governance**:
   - Manage state transitions between `working branch`/`feature/draft-*` (`.drafts/`) and `main` branch (`knowledge/`).
3. **Git SSH & Token Security (`NFR-SEC-02`)**:
   - Store GitHub/GitLab remote credentials (SSH Private Keys, OAuth Tokens) in OS Secure Keychain.
   - Enforce TLS 1.3 encryption for remote push/pull sync.

## Key Interfaces & REST Endpoints
- **Method**: `commit(file_paths: List[str], message: str, author: str) -> str`
- **Method**: `get_diff(commit_a: str, commit_b: str) -> DiffResultDTO`
- **Method**: `get_history(limit: int) -> List[CommitDTO]`
- **Method**: `rollback(commit_hash: str) -> bool`
- **Method**: `sync_remote(remote_name: str, branch: str) -> SyncStatusDTO`
- **REST Endpoints**: `GET /api/v1/git/status`, `GET /api/v1/git/history`, `GET /api/v1/git/diff`, `POST /api/v1/git/commit`, `POST /api/v1/git/sync`, `POST /api/v1/git/rollback`
- **LLM Agent Tool**: `knowledge_git_commit`

## 🚨 Strict Implementation & Quality Rules
- **Performance Benchmark (`NFR-PERF-03`)**: Git `commit` and `diff` execution latency must be **< 500ms**.
- **Pre-commit Pre-requisite Hook**: Block direct commits of `author_type: ai_generated` files to `main` branch without explicit approval decision (`NFR-SEC-01`).
