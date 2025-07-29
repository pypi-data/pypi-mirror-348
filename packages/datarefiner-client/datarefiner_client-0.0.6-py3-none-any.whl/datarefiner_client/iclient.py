from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from requests import Session


class IDataRefinerClient(ABC):
    @property
    @abstractmethod
    def _base_url(self) -> str:
        ...

    @property
    @abstractmethod
    def session(self) -> Session:
        ...

    @abstractmethod
    def _make_request(self, url: str, method: str = "GET", *args: object, **kwargs: object) -> Optional[Dict[str, Any]]:
        ...
