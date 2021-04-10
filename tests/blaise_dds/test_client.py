import pytest
import responses

from blaise_dds import StateValidationException


@responses.activate
def test_update_state_invalid_state(client, states):
    responses.add(
        responses.GET,
        "http://localhost/v1/state/descriptions",
        json=states,
    )
    with pytest.raises(StateValidationException) as error:
        client.update_state("filename", "invalid")
    assert (
        str(error.value)
        == "State 'invalid' is invalid, valid states are [inactive, started, generated, in_staging, encrypted, in_nifi_bucket, nifi_notified, in_arc, errored]"  # noqa: E501
    )


@responses.activate
def test_update_state_valid_state(client, states):
    responses.add(
        responses.GET,
        "http://localhost/v1/state/descriptions",
        json=states,
    )
    responses.add(responses.PATCH, "http://localhost/v1/state/filename")
    client.update_state("filename", "in_arc")
    assert len(responses.calls) == 2
    print(dir(responses.calls[1].request))
    assert responses.calls[1].request.body == b'{"state": "in_arc"}'


@responses.activate
def test_update_state_valid_state_an_error_info(client, states):
    responses.add(
        responses.GET,
        "http://localhost/v1/state/descriptions",
        json=states,
    )
    responses.add(responses.PATCH, "http://localhost/v1/state/filename")
    client.update_state("filename", "errored", "Massive explosions!")
    assert len(responses.calls) == 2
    print(dir(responses.calls[1].request))
    assert (
        responses.calls[1].request.body
        == b'{"state": "errored", "error_info": "Massive explosions!"}'
    )


@responses.activate
def test_get_states(client, states):
    responses.add(
        responses.GET,
        "http://localhost/v1/state/descriptions",
        json=states,
    )
    assert client.get_states() == states
    client.get_states()
    assert len(responses.calls) == 1


@responses.activate
def test_get_states_does_not_fetch_if_populated(client):
    responses.add(responses.GET, "http://localhost/v1/state/descriptions")
    client.states = {"foo": "bar"}
    assert client.get_states() == {"foo": "bar"}
    client.get_states()
    client.get_states()
    client.get_states()
    client.get_states()
    assert len(responses.calls) == 0


def test_state_is_valid(client, states):
    client.states = states
    assert client.state_is_valid("in_arc") is True


def test_state_is_valid_invalid(client, states):
    client.states = states
    assert client.state_is_valid("foobar") is False
