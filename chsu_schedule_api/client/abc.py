from abc import ABC, abstractmethod
from types import TracebackType
from typing import Self


class ABCHttpClient(ABC):
    """
    Abstract http client class.
    If you want to implement your own
    client, you should inherit this class.
    """

    @abstractmethod
    def __init__(self, *args, **kwargs) -> None: ...

    @abstractmethod
    async def request(
        self, method: str, url: str, data: object = None, **kwargs
    ) -> str | None:
        """Make a raw http request."""

    @abstractmethod
    async def request_json(
        self, method: str, url: str, data: object = None, **kwargs
    ) -> dict | list | str | int:
        """Make a json http request."""

    @abstractmethod
    async def close(self) -> None:
        """Close http session."""

    async def __aenter__(self) -> Self:
        """Enter async context manager."""
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Exit async context manager."""
        await self.close()
