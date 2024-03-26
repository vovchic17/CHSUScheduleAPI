from datetime import datetime
from typing import TYPE_CHECKING

from chsu_api.client.aiohttp import AiohttpClient
from chsu_api.constants import (
    AUDITORIUM,
    AUTH_SIGNIN,
    AUTH_VALID,
    BUILDING,
    DEPARTMENT,
    DISCIPLINE,
    STUDENT_GROUP,
    TEACHER,
    TIMETABLE,
)
from chsu_api.enums import Methods
from chsu_api.errors import CHSUApiResponseError
from chsu_api.models.auditorium import Auditorium
from chsu_api.models.building import Building
from chsu_api.models.department import Department
from chsu_api.models.discipline import Discipline
from chsu_api.models.student_group import StudentGroup
from chsu_api.models.teacher import Teacher
from chsu_api.models.timetable import TimeTable

from .abc import ABCApi

if TYPE_CHECKING:
    from chsu_api.client.abc import ABCHttpClient
    from chsu_api.models.timetable import TimeTableType


class CHSUApi(ABCApi):
    """CHSU API wrapper"""

    def __init__(
        self,
        username: str,
        password: str,
        client: "ABCHttpClient | None" = None,
    ) -> None:
        self._headers = {"User-Agent": "/"}
        self._auth_data = {"username": username, "password": password}
        self._client = client or AiohttpClient()

    async def auth_signin(self) -> True:
        """
        Authorize
        Returns true on success
        """
        resp = await self.request_json(
            Methods.POST,
            AUTH_SIGNIN,
            json=self._auth_data,
            headers=self._headers,
        )
        if isinstance(resp, dict):
            if resp.get("error", object) is None:
                self._headers["Authorization"] = f'Bearer {resp["data"]}'
                return True
            raise CHSUApiResponseError(resp["code"], resp["description"])
        raise CHSUApiResponseError(resp)

    async def auth_valid(self, token: str) -> bool:
        """Check if the token is valid"""
        resp = await self.request_json(
            Methods.POST,
            AUTH_VALID,
            data=token,
            headers=self._headers,
        )
        return bool(resp)

    async def get_buildings(self) -> list[Building]:
        """Get building list"""
        resp = await self.request_json(
            Methods.GET, BUILDING, headers=self._headers
        )
        return [Building.model_validate(bld) for bld in resp]

    async def get_student_groups(self) -> list[StudentGroup]:
        """Get student group list"""
        resp = await self.request_json(
            Methods.GET, STUDENT_GROUP, headers=self._headers
        )
        return [StudentGroup.model_validate(gr) for gr in resp]

    async def get_departments(self) -> Department:
        """Get department list"""
        resp = await self.request_json(
            Methods.GET, DEPARTMENT, headers=self._headers
        )
        return Department.model_validate(resp)

    async def get_auditoriums(self) -> list[Auditorium]:
        """Get auditorium list"""
        resp = await self.request_json(
            Methods.GET, AUDITORIUM, headers=self._headers
        )
        return [Auditorium.model_validate(aud) for aud in resp]

    async def get_numweek(self, date: datetime) -> int:
        """Get number of week by date"""
        resp = await self.request_json(
            Methods.GET,
            TIMETABLE + f"/numweek/{date.strftime("%d.%m.%Y")}/",
            headers=self._headers,
        )
        if isinstance(resp, int):
            return resp
        raise CHSUApiResponseError(resp)

    async def get_time_table(
        self, time_table: "TimeTableType"
    ) -> list[TimeTable]:
        """Get timetable"""
        resp = await self.request_json(
            Methods.GET,
            TIMETABLE + time_table.path,
            headers=self._headers,
        )
        if isinstance(resp, list):
            return [TimeTable.model_validate(tt) for tt in resp]
        raise CHSUApiResponseError(resp)

    async def get_disciplines(self) -> list[Discipline]:
        """Get discipline list"""
        resp = await self.request_json(
            Methods.GET, DISCIPLINE, headers=self._headers
        )
        return [Discipline.model_validate(dsc) for dsc in resp]

    async def get_teachers(self) -> list[Teacher]:
        """Get teacher list"""
        resp = await self.request_json(
            Methods.GET, TEACHER, headers=self._headers
        )
        return [Teacher.model_validate(tch) for tch in resp]
