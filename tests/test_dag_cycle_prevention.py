"""
Automated Test Suite for Kahn's Algorithm DAG Cycle Prevention (NFR-RELI-03)
"""

import pytest
from src.indexer.ref_dag_indexer_engine import RefDAGIndexerEngine, CircularDependencyException, Node, Edge


def test_complex_dag_cycle_detection():
    """
    Tests topological cycle detection on multi-node DAG topologies (Primary and Sub-block nodes).
    Topology:
      nodeA -> nodeB -> nodeC#section1
    Attempting to add edge nodeC#section1 -> nodeA must raise CircularDependencyException.
    """
    indexer = RefDAGIndexerEngine()
    indexer.nodes["nodeA"] = Node("nodeA", "A", "concept", "production", "human_authored", "A.md", "hashA")
    indexer.nodes["nodeB"] = Node("nodeB", "B", "concept", "production", "human_authored", "B.md", "hashB")
    indexer.nodes["nodeC#section1"] = Node("nodeC#section1", "C Sec 1", "subblock", "production", "human_authored", "C.md", "hashC", True, "nodeC")

    # Add valid edges
    e1 = Edge(source="nodeA", target="nodeB", type="references")
    e2 = Edge(source="nodeB", target="nodeC#section1", type="references")
    indexer.edges.extend([e1, e2])

    # Adding non-cyclic edge nodeA -> nodeC#section1 is valid
    valid_edge = Edge(source="nodeA", target="nodeC#section1", type="depends_on")
    assert indexer.validate_dag_cycle(valid_edge) is True

    # Adding cyclic edge nodeC#section1 -> nodeA MUST raise CircularDependencyException
    cyclic_edge = Edge(source="nodeC#section1", target="nodeA", type="references")
    with pytest.raises(CircularDependencyException) as exc_info:
        indexer.validate_dag_cycle(cyclic_edge)

    assert "Circular reference detected" in str(exc_info.value)
