import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class Config:
    url: str
    client_id: Optional[str] = None

    @classmethod
    def from_env(cls):
        cls.url = os.getenv("DDS_URL")
        cls.client_id = os.getenv("CLIENT_ID")
        return cls
