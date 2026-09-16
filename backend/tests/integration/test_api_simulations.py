from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_endpoint() -> None:
	response = client.get("/health")

	assert response.status_code == 200
	assert response.json() == {"status": "ok"}


def test_health_endpoint_allows_frontend_origin() -> None:
	response = client.get(
		"/health",
		headers={"Origin": "http://localhost:3000"},
	)

	assert response.status_code == 200
	assert response.headers["access-control-allow-origin"] == "http://localhost:3000"
