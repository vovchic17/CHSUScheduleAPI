from aiohttp import ClientSession

from chsu_schedule_api.errors import CHSUApiResponseError

from .abc import ABCHttpClient


class AiohttpClient(ABCHttpClient):
    """Http-client based on aiohttp"""

    def __init__(self, session: ClientSession | None = None) -> None:
        self._session = session

    async def request(
        self, method: str, url: str, data: object = None, **kwargs
    ) -> str | None:
        """Make an aiohttp raw request"""
        if not self._session:
            self._session = ClientSession()
        response = await self._session.request(
            method=method, url=url, data=data, **kwargs
        )
        return await response.text()

    async def request_json(
        self, method: str, url: str, data: object = None, **kwargs
    ) -> dict | list | str | int:
        """Make an aiohttp raw request"""
        if not self._session:
            self._session = ClientSession()

        response = await self._session.request(
            method=method, url=url, data=data, **kwargs
        )
        if "Пожалуйста авторизуйтесь" in await response.text():
            raise CHSUApiResponseError(response.status, "Unauthorized")
        if response.content_type != "application/json":
            raise CHSUApiResponseError(
                response.status,
                "Invalid response content type",
                response.content_type,
            )
        return await response.json()

    async def close(self) -> None:
        """Close aiohttp session"""
        if self._session and not self._session.closed:
            await self._session.close()

    def __del__(self) -> None:
        """Close session connector"""
        if (
            self._session
            and not self._session.closed
            and self._session._connector is not None  # noqa: SLF001
            and self._session._connector_owner  # noqa: SLF001
        ):
            self._session._connector._close()  # noqa: SLF001
