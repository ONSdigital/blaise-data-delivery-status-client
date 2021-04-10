import pytest
import responses

from blaise_dds import StateValidationException


def test_update_state_invalid_state(client):
    with pytest.raises(StateValidationException) as error:
        client.update_state("filename", "invalid")
    assert (
        str(error.value)
        == "State 'invalid' is invalid, valid states are [inactive, started, generated, in_staging, encrypted, in_nifi_bucket, nifi_notified, in_arc, errored]"  # noqa: E501
    )


@responses.activate
def test_update_state_valid_state(client):
    responses.add(responses.PATCH, "http://localhost/v1/state/filename")
    client.update_state("filename", "in_arc")
    assert len(responses.calls) == 1
    print(dir(responses.calls[0].request))
    assert responses.calls[0].request.body == b'{"state": "in_arc"}'


@responses.activate
def test_update_state_valid_state_an_error_info(client):
    responses.add(responses.PATCH, "http://localhost/v1/state/filename")
    client.update_state("filename", "errored", "Massive explosions!")
    assert len(responses.calls) == 1
    print(dir(responses.calls[0].request))
    assert (
        responses.calls[0].request.body
        == b'{"state": "errored", "error_info": "Massive explosions!"}'
    )
