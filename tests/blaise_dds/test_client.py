from unittest import mock

import pytest
import responses
from google.oauth2 import id_token

from blaise_dds import Client, StateValidationException


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
    assert (
        responses.calls[1].request.body
        == b'{"state": "errored", "error_info": "Massive explosions!"}'
    )


@responses.activate
def test_get_batches(client, batches):
    responses.add(
        responses.GET,
        "http://localhost/v1/batch",
        json=batches,
    )
    assert client.get_batches() == batches


@responses.activate
def test_get_batch_states(client, batch):
    batch_name = batch[0]["batch"]
    responses.add(
        responses.GET,
        f"http://localhost/v1/batch/{batch_name}",
        json=batch,
    )
    assert client.get_batch_states(batch_name) == batch


@responses.activate
def test_set_alerted(client):
    responses.add(
        responses.PATCH, "http://localhost/v1/state/filename/alerted", json={}
    )
    client.set_alerted("filename")
    assert len(responses.calls) == 1
    assert responses.calls[0].request.body == b'{"alerted": true}'


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


@mock.patch.object(Client, "token_valid")
def test_auth_token_already_valid(mock_token_valid, client):
    mock_token_valid.return_value = True
    client.jwt_token = "my fake valid token"
    client.auth_token() == "my fake valid token"


@mock.patch.object(id_token, "fetch_id_token")
@mock.patch.object(Client, "token_valid")
def test_auth_token_invalid(mock_token_valid, mock_fetch_id_token, client):
    mock_token_valid.return_value = False
    mock_fetch_id_token.return_value = "a brand new token"
    client.jwt_token = "my fake invalid token"
    client.auth_token() == "a brand new token"


@mock.patch.object(id_token, "verify_oauth2_token")
def test_token_valid_valid(_mock_verify, client):
    assert client.token_valid() is True


@mock.patch.object(id_token, "verify_oauth2_token")
def test_token_valid_invalid(mock_verify, client):
    mock_verify.side_effect = Exception("explosions")
    assert client.token_valid() is False
