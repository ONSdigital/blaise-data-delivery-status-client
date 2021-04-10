from dataclasses import dataclass
from typing import Optional


@dataclass
class Config:
    url: str
    client_id: Optional[str] = None
