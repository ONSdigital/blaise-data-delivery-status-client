import pytest

from blaise_dds.client import Client
from blaise_dds.config import Config


@pytest.fixture
def client():
    return Client(Config(url="http://localhost"))
