from typing import Dict, List, TYPE_CHECKING

from app.domain.entities import Entity, EntityId, EntityType
from app.domain.relationships import Relationship, RelationshipType

if TYPE_CHECKING:
	from app.domain.services.snapshot_service import HistoricalSnapshot


class TemporalGraph:
	def __init__(
		self,
		entities: Dict[EntityId, Entity] = None,
		relationships: Dict[EntityId, Relationship] = None,
		adj: Dict[EntityId, List[EntityId]] = None,
	) -> None:
		self.entities = dict(entities or {})
		self.relationships = dict(relationships or {})
		self.adj = {entity_id: list(targets) for entity_id, targets in (adj or {}).items()}

	@classmethod
	def from_snapshot(cls, snapshot: "HistoricalSnapshot") -> "TemporalGraph":
		entities = {
			record.id: Entity(
				id=record.id,
				type=EntityType(record.type.lower()),
				name=record.name,
				valid_from=record.valid_from,
				valid_to=record.valid_to,
				attributes=dict(record.attributes or {}),
			)
			for record in snapshot.entities
		}
		relationships = {
			record.id: Relationship(
				id=record.id,
				source_id=record.source_id,
				target_id=record.target_id,
				type=RelationshipType(record.type.lower()),
				valid_from=record.valid_from,
				valid_to=record.valid_to,
				weight=record.weight,
				confidence=record.confidence,
			)
			for record in snapshot.relationships
		}
		adjacency: Dict[EntityId, List[EntityId]] = {entity_id: [] for entity_id in entities}
		for relationship in relationships.values():
			adjacency[relationship.source_id].append(relationship.target_id)

		return cls(entities=entities, relationships=relationships, adj=adjacency)

	def neighbors(self, entity_id: EntityId) -> List[EntityId]:
		return list(self.adj.get(entity_id, []))

	def path_between(self, source_id: EntityId, target_id: EntityId) -> List[EntityId]:
		from app.domain.graph.pathfinder import PathFinder

		return PathFinder(self).shortest_path(source_id, target_id)

	def degree_centrality(self, as_of=None) -> Dict[EntityId, float]:
		from app.domain.graph.centrality import degree_centrality

		return degree_centrality(self)

	def betweenness_centrality(self, as_of=None) -> Dict[EntityId, float]:
		from app.domain.graph.centrality import betweenness_centrality

		return betweenness_centrality(self)

	def pagerank(self, as_of=None) -> Dict[EntityId, float]:
		from app.domain.graph.centrality import pagerank

		return pagerank(self)
