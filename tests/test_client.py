import pytest
from teampy import APIClient

# @pytest.fixture(scope='module')
# def api_client():
#     return APIClient(
#         instance="http://localhost:8080",
#         username="DOMAIN\myuser",
#         access_token="mock_token"
#     )


def test_api_client_instance(api_client):
    assert api_client.instance == "http://localhost:8080"


def test_api_client_username(api_client):
    assert api_client.username == "DOMAIN\myuser"


def test_api_client_access_token(api_client):
    assert api_client.access_token == "mock_token"


def test_api_client_headers(api_client):
    assert api_client.headers == {
        "content-type": "application/json",
        "accept": "application/json"
    }


def test_api_client_request_params(api_client):
    assert api_client.request_params == {"api-version": "2.0"}


def test_api_client__url(api_client):
    url = api_client._url("some_area", "some_resource")
    assert url == ("http://localhost:8080/tfs/DefaultCollection/_apis"
                   "/some_area/some_resource")


