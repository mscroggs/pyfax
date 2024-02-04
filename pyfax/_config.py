"""Configuration."""

import os
from typing import Any, Dict


class Config:
    """A class to store config variables."""
    _entries: Dict[str, Any] = {}

    def __getattr__(self, a: str) -> Any:
        """Get a config variable.

        Args:
            a: The config variable.
        """
        if a in self._entries:
            return self._entries[a]
        return None

    def __setattr__(self, a: str, b: Any):
        """Set a config variable.

        Args:
            a: The config variable.
            b: The value.
        """
        self._entries[a] = b


config = Config()
config.build_dir = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    os.path.join("..", "_pages"))
