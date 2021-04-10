from typing import Optional

import requests
from google.auth.transport.requests import Request
from google.oauth2 import id_token

from .config import Config
from .exceptions import StateValidationException
from .states import state_is_valid


class Client:
    def __init__(self, config: Config) -> None:
        self.config = config

    def update_state(
        self, filename: str, state: str, error_info: Optional[str] = None
    ) -> requests.Response:
        if not state_is_valid(state):
            raise StateValidationException(state)
        payload = {"state": state}
        headers = {}
        if error_info:
            payload["error_info"] = error_info
        if self.config.client_id:
            headers = {"Authorization": f"Bearer {self.auth_token()}"}
        return requests.patch(self._update_url(filename), json=payload, headers=headers)

    def _update_url(self, filename: str) -> str:
        return f"{self.config.url}/v1/state/{filename}"

    def auth_token(self) -> str:
        return id_token.fetch_id_token(Request(), self.config.client_id)
