from aiohttp import ClientSession

from chsu_schedule_api.errors import (
    CHSUApiResponseError,
    CHSUApiUnauthorizedError,
)

from .abc import ABCHttpClient


class AiohttpClient(ABCHttpClient):
    """Http-client based on aiohttp."""

    __slots__ = ("_session",)

    def __init__(self, session: ClientSession | None = None) -> None:
        self._session = session

    async def request(
        self, method: str, url: str, data: object = None, **kwargs
    ) -> str | None:
        """
        Make an aiohttp request.

        :param method: method for the request
        :param url: request url
        :param data: query string, defaults to None
        :return: response data
        """
        if not self._session:
            self._session = ClientSession()
        response = await self._session.request(
            method=method, url=url, data=data, **kwargs
        )
        return await response.text()

    async def request_json(
        self, method: str, url: str, data: object = None, **kwargs
    ) -> dict | list | str | int:
        """
        Make an aiohttp request.

        :param method: method for the request
        :param url: request url
        :param data: query string, defaults to None
        :raises CHSUApiUnauthorizedError:
        :raises CHSUApiResponseError:
        :return: response json data
        """
        if not self._session:
            self._session = ClientSession()

        response = await self._session.request(
            method=method, url=url, data=data, **kwargs
        )
        if "Пожалуйста авторизуйтесь" in await response.text():
            raise CHSUApiUnauthorizedError
        if response.content_type != "application/json":
            raise CHSUApiResponseError(
                response.status,
                "Invalid response content type",
                response.content_type,
            )
        return await response.json()

    async def close(self) -> None:
        """Close aiohttp session."""
        if self._session and not self._session.closed:
            await self._session.close()

    def __del__(self) -> None:
        """Close session connector."""
        if not self._session.closed:
            self._session.connector.close()
