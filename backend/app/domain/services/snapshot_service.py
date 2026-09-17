from dataclasses import dataclass
from datetime import date
from typing import List

from app.infrastructure.db.models import EntityRecord, RelationshipRecord
from app.infrastructure.repositories.entity_repo import EntityRepository
from app.infrastructure.repositories.relationship_repo import RelationshipRepository


@dataclass(frozen=True)
class HistoricalSnapshot:
	as_of: date
	entities: List[EntityRecord]
	relationships: List[RelationshipRecord]


class SnapshotService:
	def __init__(
		self,
		entity_repository: EntityRepository,
		relationship_repository: RelationshipRepository,
	) -> None:
		self.entity_repository = entity_repository
		self.relationship_repository = relationship_repository

	def create_snapshot(self, as_of: date) -> HistoricalSnapshot:
		entities = self.entity_repository.list_active_on(as_of)
		entity_ids = {entity.id for entity in entities}
		relationships = self.relationship_repository.list_active_on(as_of)
		active_relationships = [
			relationship
			for relationship in relationships
			if relationship.source_id in entity_ids and relationship.target_id in entity_ids
		]

		return HistoricalSnapshot(
			as_of=as_of,
			entities=entities,
			relationships=active_relationships,
		)
