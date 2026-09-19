from datetime import date

from fastapi.testclient import TestClient

from app.api.deps import get_db
from app.api.routers import entities as entities_router
from app.api.routers import graph as graph_router
from app.domain.services.snapshot_service import HistoricalSnapshot
from app.main import app
from app.infrastructure.db.models import EntityRecord, RelationshipRecord


ENTITY_ONE = "11111111-1111-1111-1111-111111111111"
ENTITY_TWO = "22222222-2222-2222-2222-222222222222"
RELATIONSHIP_ID = "33333333-3333-3333-3333-333333333333"


class FakeEntityRepository:
	def __init__(self, db) -> None:
		self.entities = {
			ENTITY_ONE: EntityRecord(
				id=ENTITY_ONE,
				type="person",
				name="Rhaenyra Targaryen",
				attributes={"faction": "Black"},
			),
			ENTITY_TWO: EntityRecord(id=ENTITY_TWO, type="house", name="House Stark"),
		}

	def get_by_id(self, entity_id):
		return self.entities.get(str(entity_id))

	def list_active_on(self, as_of):
		return list(self.entities.values())


class FakeRelationshipRepository:
	def __init__(self, db) -> None:
		self.relationship = RelationshipRecord(
			id=RELATIONSHIP_ID,
			source_id=ENTITY_ONE,
			target_id=ENTITY_TWO,
			type="political_support",
			weight=0.9,
			confidence=0.8,
		)

	def list_for_entity(self, entity_id, as_of=None):
		return [self.relationship]

	def list_active_on(self, as_of):
		return [self.relationship]


class FakeSnapshotService:
	def __init__(self, entity_repository, relationship_repository) -> None:
		self.snapshot = HistoricalSnapshot(
			as_of=date(125, 1, 1),
			entities=list(entity_repository.entities.values()),
			relationships=[relationship_repository.relationship],
		)

	def create_snapshot(self, as_of):
		return self.snapshot


client = TestClient(app)


def setup_module() -> None:
	app.dependency_overrides[get_db] = lambda: object()
	entities_router.EntityRepository = FakeEntityRepository
	entities_router.RelationshipRepository = FakeRelationshipRepository
	graph_router.EntityRepository = FakeEntityRepository
	graph_router.RelationshipRepository = FakeRelationshipRepository
	graph_router.SnapshotService = FakeSnapshotService


def teardown_module() -> None:
	app.dependency_overrides.clear()


def test_entity_and_graph_routes_are_registered() -> None:
	route_paths = {route.path for route in app.routes}

	assert "/v1/entities/{entity_id}" in route_paths
	assert "/v1/entities/{entity_id}/relationships" in route_paths
	assert "/v1/graph/snapshot" in route_paths
	assert "/v1/graph/path" in route_paths


def test_get_entity_returns_entity_json() -> None:
	response = client.get("/v1/entities/" + ENTITY_ONE)

	assert response.status_code == 200
	assert response.json()["name"] == "Rhaenyra Targaryen"
	assert response.json()["attributes"] == {"faction": "Black"}


def test_get_entity_relationships_returns_relationship_json() -> None:
	response = client.get(
		"/v1/entities/" + ENTITY_ONE + "/relationships",
		params={"date": "0125-01-01"},
	)

	assert response.status_code == 200
	assert response.json()["entity_id"] == ENTITY_ONE
	assert response.json()["relationships"][0]["target_id"] == ENTITY_TWO


def test_graph_snapshot_and_path_use_historical_snapshot() -> None:
	snapshot_response = client.get("/v1/graph/snapshot", params={"date": "0125-01-01"})
	path_response = client.get(
		"/v1/graph/path",
		params={"source": ENTITY_ONE, "target": ENTITY_TWO, "date": "0125-01-01"},
	)

	assert snapshot_response.status_code == 200
	assert len(snapshot_response.json()["entities"]) == 2
	assert len(snapshot_response.json()["relationships"]) == 1
	assert path_response.status_code == 200
	assert path_response.json()["path"] == [ENTITY_ONE, ENTITY_TWO]


def test_routes_validate_uuid_and_required_dates() -> None:
	invalid_id = client.get("/v1/entities/entity-1")
	missing_date = client.get("/v1/graph/snapshot")

	assert invalid_id.status_code == 422
	assert missing_date.status_code == 422