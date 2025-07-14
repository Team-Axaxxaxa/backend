import pytest
from fastapi.testclient import TestClient

from src.utils.settings import get_settings


@pytest.mark.parametrize(
    'is_male',
    [
        pytest.param(True, id='Male'),
        pytest.param(False, id='Female')
    ]
)
def test_create_test_taker(is_male: bool, client: TestClient):
    settings = get_settings()
    response = client.post(settings.PATH_PREFIX + '/test_taker', json={'is_male': is_male})
    assert response.status_code == 200


def test_create_test_taker_invalid_json(client: TestClient):
    settings = get_settings()
    response = client.post(settings.PATH_PREFIX + '/test_taker', json={'is_male': 'okak'})
    assert response.status_code == 422
