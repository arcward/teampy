import pytest
from teampy import APIClient


@pytest.fixture(scope='module')
def api_client():
    return APIClient(
        instance="http://localhost:8080",
        username="DOMAIN\myuser",
        access_token="mock_token"
    )