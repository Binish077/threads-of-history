import pytest

from app.domain.entities import Entity, EntityType
from app.domain.graph.centrality import betweenness_centrality, degree_centrality, pagerank
from app.domain.graph.temporal_graph import TemporalGraph
from app.domain.relationships import Relationship, RelationshipType


def build_chain() -> TemporalGraph:
	entities = {
		entity_id: Entity(entity_id, EntityType.PERSON, entity_id)
		for entity_id in ("a", "b", "c")
	}
	relationships = {
		"a-b": Relationship("a-b", "a", "b", RelationshipType.ALLIANCE, weight=1.0),
		"b-c": Relationship("b-c", "b", "c", RelationshipType.ALLIANCE, weight=1.0),
	}
	return TemporalGraph(
		entities=entities,
		relationships=relationships,
		adj={"a": ["b"], "b": ["c"], "c": []},
	)


def test_degree_centrality_counts_incoming_and_outgoing_links() -> None:
	graph = build_chain()

	assert degree_centrality(graph) == {"a": 0.5, "b": 1.0, "c": 0.5}
	assert graph.degree_centrality() == degree_centrality(graph)


def test_betweenness_centrality_uses_directed_weighted_paths() -> None:
	graph = build_chain()

	scores = betweenness_centrality(graph)

	assert scores["a"] == 0.0
	assert scores["b"] == pytest.approx(0.5)
	assert scores["c"] == 0.0
	assert graph.betweenness_centrality() == scores


def test_pagerank_returns_normalized_scores_and_ranks_chain_middle_highest() -> None:
	graph = build_chain()

	scores = pagerank(graph)

	assert sum(scores.values()) == pytest.approx(1.0)
	assert scores["c"] > scores["b"] > scores["a"]
	assert graph.pagerank() == scores


def test_pagerank_rejects_invalid_damping() -> None:
	with pytest.raises(ValueError):
		pagerank(build_chain(), damping=1.0)