import pytest
from configparser import ConfigParser
from teampy import APIClient


# @pytest.fixture(scope="module")
# def api_client():
#     parser = ConfigParser()
#     parser.read('conf.ini')
#     return APIClient(
#         parser['DEFAULT']['instance'],
#         parser['DEFAULT']['username'],
#         parser['DEFAULT']['access_token']
#     )

@pytest.fixture(scope='module')
def api_client():
    return APIClient(
        instance="http://localhost:8080",
        username="DOMAIN\myuser",
        access_token="mock_token"
    )