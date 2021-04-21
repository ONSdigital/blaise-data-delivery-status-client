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


@pytest.fixture
def batches():
    return [
        "BATCH1",
        "BATCH2",
        "BATCH3",
        "BATCH4",
        "BATCH5",
    ]


@pytest.fixture
def batch():
    return [
        {
            "batch": "24032021_165033",
            "dd_filename": "dd_OPN2102R_24032021_165033.zip",
            "state": "Started",
            "updated_at": "2021-03-24T16:50:35+00:00",
            "alerted": False,
        },
        {
            "batch": "24032021_165033",
            "dd_filename": "dd_OPN2101W_24032021_165033.zip",
            "state": "in_staging",
            "updated_at": "2021-03-24T16:50:35+00:00",
            "alerted": False,
        },
    ]
