import pytest

from blaise_dds.client import Client
from blaise_dds.config import Config


@pytest.fixture
def client():
    return Client(Config(url="http://localhost"))


@pytest.fixture
def states():
    return {
        "inactive": "",
        "started": "",
        "generated": "",
        "in_staging": "",
        "encrypted": "",
        "in_nifi_bucket": "",
        "nifi_notified": "",
        "in_arc": "",
        "errored": "",
    }
