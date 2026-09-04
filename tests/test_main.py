from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_package_strips_whitespace() -> None:
    response = client.post(
        "/packages",
        json={"name": " fastapi ", "version": " 0.63.0 "},
    )

    assert response.status_code == 200
    assert response.json() == {"name": "fastapi", "version": "0.63.0"}


def test_create_package_rejects_matching_name_and_version() -> None:
    response = client.post(
        "/packages",
        json={"name": "same", "version": "same"},
    )

    assert response.status_code == 422
