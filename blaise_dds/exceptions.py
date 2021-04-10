from typing import Dict


class StateValidationException(Exception):
    def __init__(self, state: str, states: Dict[str, str]) -> None:
        self.state = state
        self.valid_states = ", ".join(states.keys())
        super().__init__(
            f"State '{self.state}' is invalid, valid states are [{self.valid_states}]"
        )
