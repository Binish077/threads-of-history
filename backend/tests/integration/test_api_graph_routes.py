from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_entity_and_graph_routes_are_registered() -> None:
	route_paths = {route.path for route in app.routes}

	assert "/v1/entities/{entity_id}" in route_paths
	assert "/v1/entities/{entity_id}/relationships" in route_paths
	assert "/v1/graph/snapshot" in route_paths
	assert "/v1/graph/path" in route_paths


def test_entity_route_is_a_typed_not_implemented_skeleton() -> None:
	response = client.get("/v1/entities/entity-1")

	assert response.status_code == 501
	assert response.json() == {"detail": "Entity retrieval is not implemented yet"}


def test_graph_routes_validate_inputs_before_handler_execution() -> None:
	missing_date = client.get("/v1/graph/snapshot")
	path_skeleton = client.get(
		"/v1/graph/path",
		params={"source": "entity-1", "target": "entity-2"},
	)

	assert missing_date.status_code == 422
	assert path_skeleton.status_code == 501