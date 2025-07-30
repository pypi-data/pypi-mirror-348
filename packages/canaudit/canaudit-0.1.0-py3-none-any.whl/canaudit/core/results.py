from dataclasses import dataclass
from typing import Literal


@dataclass
class Finding:
    module: str
    id: str
    timestamp: float
    issue: str
    severity: Literal["low", "medium", "high"]
    description: str = ""
