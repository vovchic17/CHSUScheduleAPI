from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from chsu_schedule_api.constants import BASE_URL

if TYPE_CHECKING:
    from chsu_schedule_api.client.abc import ABCHttpClient
    from chsu_schedule_api.enums import Methods


class ABCApi(ABC):
    """Abstract API class"""

    _client: "ABCHttpClient"
    _auth_data: dict[str, str]
    _headers: dict[str, str]

    @abstractmethod
    def __init__(
        self, username: str, password: str, client: "ABCHttpClient | None"
    ) -> None: ...

    async def request(
        self, method: "Methods", path: str, data: object = None, **kwargs
    ) -> str | None:
        """Make http request"""
        return await self._client.request(
            method, f"{BASE_URL}{path}", data=data, **kwargs
        )

    async def request_json(
        self, method: "Methods", path: str, data: object = None, **kwargs
    ) -> dict | list | str | int:
        """Make http request"""
        return await self._client.request_json(
            method, f"{BASE_URL}{path}", data=data, **kwargs
        )
