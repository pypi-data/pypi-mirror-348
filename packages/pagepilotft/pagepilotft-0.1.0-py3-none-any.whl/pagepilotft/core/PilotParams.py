from typing import Optional


class PilotParams:
    def __init__(self, params: Optional[dict] = None):
        self._params = params or {}

    def get(self, key: str):
        return self._params.get(key)

    def get_all(self) -> dict:
        return self._params
