/**
 * Git Management Dashboard & Visual Diff Viewer Component (DSGN-UI-DASHBOARD)
 *
 * Provides Web UI controls for Git repository status, commit timelines,
 * line-by-line visual diff comparison, and human approval decision widgets.
 */

import React, { useState, useEffect } from 'react';

export interface CommitDTO {
  commit_hash: str;
  author: str;
  message: str;
  timestamp: number;
  changed_files: string[];
}

export interface DiffResultDTO {
  commit_a: string;
  commit_b: string;
  diff_text: string;
  additions: number;
  deletions: number;
  files_changed: string[];
}

export interface PendingApprovalDTO {
  node_id: string;
  title: string;
  type: string;
  author_type: string;
  extracted_markdown: string;
}

export const GitManagementDashboard: React.FC = () => {
  const [status, setStatus] = useState<{ branch: string; unstaged_count: number }>({
    branch: 'main',
    unstaged_count: 0
  });
  const [history, setHistory] = useState<CommitDTO[]>([]);
  const [pendingApprovals, setPendingApprovals] = useState<PendingApprovalDTO[]>([]);
  const [selectedDiff, setSelectedDiff] = useState<DiffResultDTO | null>(null);

  useEffect(() => {
    // Mock REST API fetching
    fetchStatus();
    fetchPendingApprovals();
  }, []);

  const fetchStatus = async () => {
    // GET /api/v1/git/status
    setStatus({ branch: 'main', unstaged_count: 2 });
  };

  const fetchPendingApprovals = async () => {
    // GET /api/v1/approval/pending
    setPendingApprovals([
      {
        node_id: 'node-101',
        title: 'Fix circular dependency in graph parser',
        type: 'solution',
        author_type: 'ai_generated',
        extracted_markdown: '# Fix circular dependency...'
      }
    ]);
  };

  const handleApprovalDecision = async (nodeId: string, decision: 'approve' | 'reject') => {
    // POST /api/v1/approval/decide
    console.log(`[Human Broker Decision] Node: ${nodeId}, Decision: ${decision}`);
    setPendingApprovals((prev) => prev.filter((item) => item.node_id !== nodeId));
  };

  return (
    <div style={{ padding: '24px', fontFamily: 'sans-serif', backgroundColor: '#0f172a', color: '#f8fafc', minHeight: '100vh' }}>
      <header style={{ marginBottom: '32px', borderBottom: '1px solid #334155', pb: '16px' }}>
        <h1 style={{ fontSize: '24px', fontWeight: 'bold', color: '#38bdf8' }}>Git & Knowledge Management Dashboard</h1>
        <p style={{ color: '#94a3b8' }}>Branch: <span style={{ color: '#4ade80', fontWeight: 'bold' }}>{status.branch}</span> | Unstaged Changes: {status.unstaged_count}</p>
      </header>

      {/* Human Approval Gate Widget (NFR-SEC-01) */}
      <section style={{ marginBottom: '32px', backgroundColor: '#1e293b', padding: '20px', borderRadius: '8px' }}>
        <h2 style={{ fontSize: '18px', marginBottom: '16px', color: '#facc15' }}>Human Approval Review Queue (NFR-SEC-01)</h2>
        {pendingApprovals.length === 0 ? (
          <p style={{ color: '#64748b' }}>No pending draft nodes awaiting approval.</p>
        ) : (
          pendingApprovals.map((item) => (
            <div key={item.node_id} style={{ border: '1px solid #475569', padding: '16px', borderRadius: '6px', marginBottom: '12px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div>
                <h3 style={{ fontSize: '16px', color: '#e2e8f0', margin: '0 0 4px 0' }}>{item.title} ({item.node_id})</h3>
                <span style={{ fontSize: '12px', background: '#3b82f6', color: '#fff', padding: '2px 8px', borderRadius: '4px' }}>{item.type}</span>
                <span style={{ fontSize: '12px', background: '#e11d48', color: '#fff', padding: '2px 8px', borderRadius: '4px', marginLeft: '8px' }}>{item.author_type}</span>
              </div>
              <div>
                <button
                  onClick={() => handleApprovalDecision(item.node_id, 'approve')}
                  style={{ backgroundColor: '#22c55e', color: '#fff', border: 'none', padding: '8px 16px', borderRadius: '4px', cursor: 'pointer', marginRight: '8px' }}
                >
                  Approve & Merge
                </button>
                <button
                  onClick={() => handleApprovalDecision(item.node_id, 'reject')}
                  style={{ backgroundColor: '#ef4444', color: '#fff', border: 'none', padding: '8px 16px', borderRadius: '4px', cursor: 'pointer' }}
                >
                  Reject
                </button>
              </div>
            </div>
          ))
        )}
      </section>

      {/* Visual Diff Viewer Modal Simulation */}
      {selectedDiff && (
        <div style={{ backgroundColor: '#1e293b', padding: '20px', borderRadius: '8px', border: '1px solid #38bdf8' }}>
          <h3 style={{ color: '#38bdf8' }}>Visual Line-by-Line Diff ({selectedDiff.commit_a} vs {selectedDiff.commit_b})</h3>
          <pre style={{ backgroundColor: '#020617', padding: '16px', borderRadius: '4px', overflowX: 'auto', color: '#4ade80' }}>
            {selectedDiff.diff_text}
          </pre>
        </div>
      )}
    </div>
  );
};

export default GitManagementDashboard;
