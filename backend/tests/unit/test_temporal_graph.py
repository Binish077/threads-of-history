from datetime import date

from app.domain.entities import EntityType
from app.domain.graph.temporal_graph import TemporalGraph
from app.domain.relationships import RelationshipType
from app.domain.services.snapshot_service import HistoricalSnapshot
from app.infrastructure.db.models import EntityRecord, RelationshipRecord


def test_from_snapshot_builds_domain_objects_and_directed_adjacency() -> None:
	entity_one = EntityRecord(
		id="entity-1",
		type="person",
		name="Rhaenyra Targaryen",
		attributes={"faction": "Black"},
	)
	entity_two = EntityRecord(
		id="entity-2",
		type="house",
		name="House Stark",
	)
	relationship = RelationshipRecord(
		id="relationship-1",
		source_id="entity-1",
		target_id="entity-2",
		type="political_support",
		weight=0.9,
		confidence=0.8,
	)
	snapshot = HistoricalSnapshot(
		as_of=date(125, 1, 1),
		entities=[entity_one, entity_two],
		relationships=[relationship],
	)

	graph = TemporalGraph.from_snapshot(snapshot)

	assert graph.entities["entity-1"].type is EntityType.PERSON
	assert graph.entities["entity-1"].attributes == {"faction": "Black"}
	assert graph.relationships["relationship-1"].type is RelationshipType.POLITICAL_SUPPORT
	assert graph.relationships["relationship-1"].weight == 0.9
	assert graph.neighbors("entity-1") == ["entity-2"]
	assert graph.neighbors("entity-2") == []

	entity_one.attributes["faction"] = "Green"
	assert graph.entities["entity-1"].attributes == {"faction": "Black"}


def test_neighbors_returns_a_copy() -> None:
	graph = TemporalGraph(adj={"entity-1": ["entity-2"]})

	neighbors = graph.neighbors("entity-1")
	neighbors.append("entity-3")

	assert graph.neighbors("entity-1") == ["entity-2"]
