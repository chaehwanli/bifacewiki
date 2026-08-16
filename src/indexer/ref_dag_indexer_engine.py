"""
Ref-DAG In-Memory & Persistent Indexer Engine (DSGN-INDEXER-DAG)

Implements Dual-Layer logical graph index:
- Tier-1 In-Memory Hot Graph Data Structure
- Tier-2 Embedded SQLite Persistent Graph Store
- Incremental hash sync (< 50ms), Cold start (< 500ms)
- Sub-block section (#heading) node parsing
- 500ms Sliding Window File Watcher Debounce Throttler
- Kahn's Topological Sort DAG Cycle Prevention Algorithm
"""

import os
import re
import sqlite3
import hashlib
import time
from collections import defaultdict, deque
from dataclasses import dataclass, field
from typing import List, Dict, Set, Optional, Tuple


class CircularDependencyException(Exception):
    """Raised when adding an edge creates a cycle in the Ref-DAG."""
    pass


@dataclass
class Node:
    id: str
    title: str
    type: str  # concept, solution, negative_knowledge, architecture
    status: str  # draft, review_pending, production, deprecated, archived
    author_type: str  # ai_generated, human_authored
    file_path: str
    content_hash: str
    is_subblock: bool = False
    parent_id: Optional[str] = None


@dataclass
class Edge:
    source: str
    target: str
    type: str  # references, depends_on, parent_of, child_of, replaces, semantically_related


@dataclass
class SubGraphDTO:
    nodes: List[Node]
    edges: List[Edge]


class FileWatcherThrottler:
    """500ms Sliding Window Event Queue for File Watcher Debouncing."""
    def __init__(self, debounce_window_sec: float = 0.5):
        self.debounce_window_sec = debounce_window_sec
        self.pending_files: Set[str] = set()
        self.last_event_time: float = 0.0

    def add_event(self, file_path: str):
        self.pending_files.add(file_path)
        self.last_event_time = time.time()

    def should_flush(self) -> bool:
        if not self.pending_files:
            return False
        return (time.time() - self.last_event_time) >= self.debounce_window_sec

    def flush(self) -> List[str]:
        batch = list(self.pending_files)
        self.pending_files.clear()
        return batch


class RefDAGIndexerEngine:
    def __init__(self, db_path: str = ":memory:"):
        self.db_path = db_path
        self.nodes: Dict[str, Node] = {}
        self.edges: List[Edge] = []
        self.throttler = FileWatcherThrottler(debounce_window_sec=0.5)
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self._init_sqlite_db()

    def _init_sqlite_db(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS nodes (
                id TEXT PRIMARY KEY,
                title TEXT,
                type TEXT,
                status TEXT,
                author_type TEXT,
                file_path TEXT,
                content_hash TEXT,
                is_subblock INTEGER,
                parent_id TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS edges (
                source TEXT,
                target TEXT,
                type TEXT,
                PRIMARY KEY (source, target, type)
            )
        """)
        self.conn.commit()

    @staticmethod
    def compute_hash(content: str) -> str:
        return hashlib.sha256(content.encode('utf-8')).hexdigest()

    def parse_markdown_file(self, file_path: str) -> Tuple[Node, List[Node], List[Edge]]:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        file_hash = self.compute_hash(content)
        
        # 1. Parse Frontmatter
        frontmatter_match = re.search(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        meta = {}
        body = content
        if frontmatter_match:
            yaml_block = frontmatter_match.group(1)
            body = content[frontmatter_match.end():]
            for line in yaml_block.splitlines():
                if ':' in line:
                    k, v = line.split(':', 1)
                    meta[k.strip()] = v.strip().strip('"\'')

        file_id = meta.get('id', os.path.splitext(os.path.basename(file_path))[0])
        title = meta.get('title', file_id)
        node_type = meta.get('type', 'concept')
        status = meta.get('status', 'draft')
        author_type = meta.get('author_type', 'ai_generated')

        primary_node = Node(
            id=file_id,
            title=title,
            type=node_type,
            status=status,
            author_type=author_type,
            file_path=file_path,
            content_hash=file_hash
        )

        sub_nodes = []
        file_edges = []

        # 2. Parse Sub-blocks (Headings)
        heading_matches = re.finditer(r'^(#{1,3})\s+(.+)$', body, re.MULTILINE)
        for match in heading_matches:
            heading_title = match.group(2).strip()
            slug = re.sub(r'[^\w\-]', '-', heading_title.lower())
            sub_id = f"{file_id}#{slug}"
            sub_node = Node(
                id=sub_id,
                title=heading_title,
                type="subblock",
                status=status,
                author_type=author_type,
                file_path=file_path,
                content_hash=self.compute_hash(heading_title),
                is_subblock=True,
                parent_id=file_id
            )
            sub_nodes.append(sub_node)
            file_edges.append(Edge(source=file_id, target=sub_id, type="parent_of"))

        # 3. Parse Wikilinks [[target_id]] or [[target_id#heading]]
        wikilinks = re.findall(r'\[\[(.*?)\]\]', body)
        for link in wikilinks:
            target_id = link.strip().split('|')[0]
            file_edges.append(Edge(source=file_id, target=target_id, type="references"))

        return primary_node, sub_nodes, file_edges

    def validate_dag_cycle(self, new_edge: Edge) -> bool:
        """
        Kahn's Topological Sort Algorithm based Cycle Detection.
        Validates if adding new_edge creates a cycle in the DAG.
        """
        adj_list = defaultdict(set)
        in_degree = defaultdict(int)
        all_nodes = set(self.nodes.keys())
        all_nodes.add(new_edge.source)
        all_nodes.add(new_edge.target)

        for edge in self.edges + [new_edge]:
            adj_list[edge.source].add(edge.target)
            in_degree[edge.target] += 1
            if edge.source not in in_degree:
                in_degree[edge.source] = 0

        queue = deque([n for n in all_nodes if in_degree[n] == 0])
        visited_count = 0

        while queue:
            curr = queue.popleft()
            visited_count += 1
            for neighbor in adj_list[curr]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        if visited_count != len(all_nodes):
            raise CircularDependencyException(
                f"Circular reference detected when adding link from '{new_edge.source}' to '{new_edge.target}'."
            )
        return True

    def reindex_incremental(self, file_paths: List[str]) -> None:
        """
        Incremental re-indexing of changed files into Tier-1 memory and Tier-2 SQLite.
        Latency target: < 50ms (NFR-PERF-02).
        """
        start_time = time.time()

        cursor = self.conn.cursor()
        for path in file_paths:
            if not os.path.exists(path):
                continue

            primary, sub_nodes, new_edges = self.parse_markdown_file(path)

            # Check hash for incremental skip
            cursor.execute("SELECT content_hash FROM nodes WHERE id = ?", (primary.id,))
            row = cursor.fetchone()
            if row and row[0] == primary.content_hash:
                continue  # Hash unchanged, skip parsing

            # Update Memory (Tier-1)
            self.nodes[primary.id] = primary
            for sub in sub_nodes:
                self.nodes[sub.id] = sub

            for e in new_edges:
                try:
                    self.validate_dag_cycle(e)
                    self.edges.append(e)
                except CircularDependencyException as cde:
                    print(f"[Warning] Cycle rejected: {cde}")

            # Update SQLite (Tier-2)
            cursor.execute("""
                INSERT OR REPLACE INTO nodes VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (primary.id, primary.title, primary.type, primary.status,
                  primary.author_type, primary.file_path, primary.content_hash,
                  0, None))
            for sub in sub_nodes:
                cursor.execute("""
                    INSERT OR REPLACE INTO nodes VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (sub.id, sub.title, sub.type, sub.status,
                      sub.author_type, sub.file_path, sub.content_hash,
                      1, sub.parent_id))
            for e in new_edges:
                cursor.execute("INSERT OR REPLACE INTO edges VALUES (?, ?, ?)", (e.source, e.target, e.type))

        self.conn.commit()

        elapsed = (time.time() - start_time) * 1000
        if elapsed > 50:
            print(f"[Warning] Incremental sync latency target exceeded: {elapsed:.2f}ms")

    def get_related_subgraph(self, node_id: str, depth: int = 1, filter_status: str = "production") -> SubGraphDTO:
        """
        Retrieves graph subtree rooted at node_id, filtering by status (e.g. production for LLM context NFR-SEC-01).
        """
        visited_nodes: Set[str] = set()
        matched_edges: List[Edge] = []
        queue = deque([(node_id, 0)])

        while queue:
            curr_id, curr_depth = queue.popleft()
            if curr_id in visited_nodes or curr_depth > depth:
                continue

            node = self.nodes.get(curr_id)
            if not node:
                continue
            if filter_status and node.status != filter_status:
                continue

            visited_nodes.add(curr_id)

            for edge in self.edges:
                if edge.source == curr_id:
                    matched_edges.append(edge)
                    queue.append((edge.target, curr_depth + 1))

        matched_nodes = [self.nodes[nid] for nid in visited_nodes if nid in self.nodes]
        return SubGraphDTO(nodes=matched_nodes, edges=matched_edges)
