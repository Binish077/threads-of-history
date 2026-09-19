from app.domain.entities import Entity, EntityType
from app.domain.graph.pathfinder import PathFinder, weighted_path
from app.domain.graph.temporal_graph import TemporalGraph
from app.domain.relationships import Relationship, RelationshipType


def build_graph() -> TemporalGraph:
	entities = {
		entity_id: Entity(entity_id, EntityType.PERSON, entity_id)
		for entity_id in ("a", "b", "c", "d")
	}
	relationships = {
		"a-b": Relationship("a-b", "a", "b", RelationshipType.ALLIANCE, weight=1.0),
		"b-c": Relationship("b-c", "b", "c", RelationshipType.ALLIANCE, weight=1.0),
		"a-c": Relationship("a-c", "a", "c", RelationshipType.ALLIANCE, weight=3.0),
	}
	return TemporalGraph(
		entities=entities,
		relationships=relationships,
		adj={"a": ["b", "c"], "b": ["c"], "c": [], "d": []},
	)


def test_pathfinder_returns_lowest_weight_directed_path() -> None:
	graph = build_graph()

	assert PathFinder(graph).shortest_path("a", "c") == ["a", "b", "c"]
	assert graph.path_between("a", "c") == ["a", "b", "c"]
	assert weighted_path(graph, "c", "a") == []


def test_pathfinder_handles_trivial_and_missing_paths() -> None:
	graph = build_graph()

	assert PathFinder(graph).find_path("a", "a") == ["a"]
	assert PathFinder(graph).shortest_path("a", "d") == []
	assert PathFinder(graph).shortest_path("missing", "c") == []