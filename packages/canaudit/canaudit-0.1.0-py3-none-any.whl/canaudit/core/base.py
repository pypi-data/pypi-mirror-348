"""
base.py

Defines the abstract base class `AuditModule` for all audit modules.

Each module implements:
- A `run()` method that accepts CAN message data and returns a list of findings
"""

from abc import ABC, abstractmethod

import pandas as pd


class AuditModule(ABC):
    """
    Abstract base class for all audit modules.
    """

    name: str = "unnamed"
    description: str = "no description"

    def __init__(self, config=None):
        self.config = config or {}

    @abstractmethod
    def run(self, messages: pd.DataFrame) -> list[dict]:
        """
        Run audit on the given CAN trace messages.
        Returns a list of finding dictionaries.
        """
        ...
