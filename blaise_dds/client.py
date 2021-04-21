from typing import Any, Dict, List, Optional

import requests
from google.auth.transport.requests import Request
from google.oauth2 import id_token

from .config import Config
from .exceptions import StateValidationException


class Client:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.states: Dict[str, str] = {}
        self.jwt_token = ""
        self.google_request = Request()

    def update_state(
        self, filename: str, state: str, error_info: Optional[str] = None
    ) -> requests.Response:
        if not self.state_is_valid(state):
            raise StateValidationException(state, self.get_states())
        payload = {"state": state}
        if error_info:
            payload["error_info"] = error_info
        return requests.patch(
            self._update_url(filename), json=payload, headers=self._headers()
        )

    def get_states(self) -> Dict[str, str]:
        if self.states == {}:
            self.states = requests.get(
                f"{self.config.url}/v1/state/descriptions", headers=self._headers()
            ).json()
        return self.states

    def get_batches(self) -> List[str]:
        return requests.get(self._batches_url(), headers=self._headers()).json()

    def get_batch_states(self, batch: str) -> List[Dict[str, Any]]:
        return requests.get(self._batch_url(batch), headers=self._headers()).json()

    def set_alerted(self, filename: str) -> Dict[str, Any]:
        payload = {"alerted": True}
        return requests.patch(
            self._alert_url(filename), json=payload, headers=self._headers()
        ).json()

    def state_is_valid(self, state: str) -> bool:
        return state in self.get_states().keys()

    def _update_url(self, filename: str) -> str:
        return f"{self.config.url}/v1/state/{filename}"

    def _batches_url(self) -> str:
        return f"{self.config.url}/v1/batch"

    def _batch_url(self, batch: str) -> str:
        return f"{self._batches_url()}/{batch}"

    def _alert_url(self, filename: str) -> str:
        return f"{self._update_url(filename)}/alerted"

    def _headers(self) -> Dict[str, str]:
        if self.config.client_id:
            return {"Authorization": f"Bearer {self.auth_token()}"}
        return {}

    def auth_token(self) -> str:
        if self.token_valid():
            return self.jwt_token
        return id_token.fetch_id_token(self.google_request, self.config.client_id)

    def token_valid(self) -> bool:
        try:
            id_token.verify_oauth2_token(self.jwt_token, self.google_request)
        except Exception:
            return False
        return True
