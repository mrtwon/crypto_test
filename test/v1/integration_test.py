import pytest
from starlette.testclient import TestClient


@pytest.mark.test_tron
class TestTron:

    @pytest.mark.parametrize("address, status_code", [
        ("TTzPiwbBedv7E8p4FkyPyeqq4RVoqRL3TW", 200),
        ("TTzPiwbBedv7E8p4FkyPyeqq4RVoqRL3T0", 404)
    ])
    def test_get_by_address(self, address: str, status_code: int, client: TestClient):
        body = {'address': address}
        result = client.post('/api/v1/tron/balance', json=body)
        assert result.status_code == status_code

    def test_get_statistics(self, client: TestClient):
        result = client.get('/api/v1/statistics')
        json_result = result.json()
        assert result.status_code == 200 and isinstance(json_result, list) and len(json_result) == 2
