from fastapi.testclient import TestClient

from src.utils.settings import get_settings


def test_get_health_ok(client: TestClient):
    settings = get_settings()
    response = client.get(f'{settings.PATH_PREFIX}/health')
    assert response.status_code == 200
