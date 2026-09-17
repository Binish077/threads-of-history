from datetime import date
from unittest.mock import MagicMock

from app.domain.services.snapshot_service import SnapshotService
from app.infrastructure.db.models import EntityRecord, RelationshipRecord


def test_create_snapshot_loads_active_records_for_date() -> None:
	as_of = date(125, 1, 1)
	entity = EntityRecord(id="entity-1", name="Rhaenyra Targaryen")
	relationship = RelationshipRecord(
		id="relationship-1",
		source_id="entity-1",
		target_id="entity-2",
		type="political_support",
	)
	entity_repository = MagicMock()
	entity_repository.list_active_on.return_value = [entity]
	relationship_repository = MagicMock()
	relationship_repository.list_active_on.return_value = [relationship]
	service = SnapshotService(entity_repository, relationship_repository)

	snapshot = service.create_snapshot(as_of)

	assert snapshot.as_of == as_of
	assert snapshot.entities == [entity]
	assert snapshot.relationships == []
	entity_repository.list_active_on.assert_called_once_with(as_of)
	relationship_repository.list_active_on.assert_called_once_with(as_of)


def test_create_snapshot_keeps_relationships_with_two_active_endpoints() -> None:
	as_of = date(125, 1, 1)
	entities = [
		EntityRecord(id="entity-1", name="Rhaenyra Targaryen"),
		EntityRecord(id="entity-2", name="House Stark"),
	]
	relationship = RelationshipRecord(
		id="relationship-1",
		source_id="entity-1",
		target_id="entity-2",
		type="political_support",
	)
	entity_repository = MagicMock()
	entity_repository.list_active_on.return_value = entities
	relationship_repository = MagicMock()
	relationship_repository.list_active_on.return_value = [relationship]

	snapshot = SnapshotService(entity_repository, relationship_repository).create_snapshot(as_of)

	assert snapshot.relationships == [relationship]