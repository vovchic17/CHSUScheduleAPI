from datetime import datetime
from typing import TYPE_CHECKING

from chsu_schedule_api.client.aiohttp import AiohttpClient
from chsu_schedule_api.constants import (
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
from chsu_schedule_api.enums import Methods
from chsu_schedule_api.errors import (
    CHSUApiLookupError,
    CHSUApiResponseError,
    CHSUApiUnauthorizedError,
)
from chsu_schedule_api.types import (
    Auditorium,
    Building,
    Department,
    Discipline,
    Group,
    GroupId,
    Lecturer,
    LecturerId,
    StudentGroup,
    Teacher,
    TimeTable,
    TitleTimeTableType,
)

from .abc import ABCApi

if TYPE_CHECKING:
    from chsu_schedule_api.client.abc import ABCHttpClient
    from chsu_schedule_api.types import TimeTableType


class CHSUApi(ABCApi):
    """CHSU API wrapper class."""

    __slots__ = ("_cache",)

    def __init__(
        self,
        username: str,
        password: str,
        client: "ABCHttpClient | None" = None,
    ) -> None:
        self._headers = {"User-Agent": "/"}
        self._auth_data = {"username": username, "password": password}
        self._cache: dict[str, dict[str, "TimeTableType"]] = {
            "lecturers": {},
            "groups": {},
        }
        super().__init__(client or AiohttpClient())

    async def auth_signin(self) -> bool:
        """
        Authorize method.

        :raises CHSUApiUnauthorizedError: Invalid auth data
        :raises CHSUApiResponseError: invalid response
        :return: On success, :code:`True` is returned.
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
            raise CHSUApiUnauthorizedError(
                resp["error"]["code"], resp["error"]["description"]
            )
        raise CHSUApiResponseError(resp)

    async def auth_valid(self, token: str) -> bool:
        """
        Validate auth token.

        :param token: auth token
        :return: If token is valid, :code:`True` is returned.
        """
        resp = await self.request_json(
            Methods.POST,
            AUTH_VALID,
            data=token,
            headers=self._headers,
        )
        return bool(resp)

    async def get_buildings(self) -> list[Building]:
        """
        Get buildings method.

        Get list of all buildings.

        :return:
        """
        resp = await self.request_json(
            Methods.GET, BUILDING, headers=self._headers
        )
        return [Building.model_validate(bld) for bld in resp]

    async def get_student_groups(self) -> list[StudentGroup]:
        """
        Get student groups method.

        Get list of all student groups.

        :return:
        """
        resp = await self.request_json(
            Methods.GET, STUDENT_GROUP, headers=self._headers
        )
        return [StudentGroup.model_validate(gr) for gr in resp]

    async def get_departments(self) -> Department:
        """
        Get departments method.

        Get departments node tree

        :return:
        """
        resp = await self.request_json(
            Methods.GET, DEPARTMENT, headers=self._headers
        )
        return Department.model_validate(resp)

    async def get_auditoriums(self) -> list[Auditorium]:
        """
        Get auditoriums method.

        Get list of all auditoriums.

        :return:
        """
        resp = await self.request_json(
            Methods.GET, AUDITORIUM, headers=self._headers
        )
        return [Auditorium.model_validate(aud) for aud in resp]

    async def get_numweek(self, date: datetime) -> int:
        """
        Get the number of the academic week for a given date.

        :param date: week date
        :raises CHSUApiResponseError: invalid response
        :return: Number of the academic week
        """
        resp = await self.request_json(
            Methods.GET,
            TIMETABLE + f"/numweek/{date.strftime("%d.%m.%Y")}/",
            headers=self._headers,
        )
        if isinstance(resp, int):
            return resp
        raise CHSUApiResponseError(resp)

    async def get_time_table(
        self, time_table: "TimeTableType | TitleTimeTableType"
    ) -> list[TimeTable]:
        """
        Get time table method.

        Get a time table for a specific lecturer, group, or get a full schedule

        :param time_table:
        :raises CHSUApiResponseError: invalid response
        :return:
        """
        if isinstance(time_table, TitleTimeTableType):
            time_table = await self._get_id_by_title(time_table)
        resp = await self.request_json(
            Methods.GET,
            TIMETABLE + time_table.path,
            headers=self._headers,
        )
        if isinstance(resp, list):
            return [TimeTable.model_validate(tt) for tt in resp]
        raise CHSUApiResponseError(resp)

    async def get_disciplines(self) -> list[Discipline]:
        """
        Get disciplines method.

        Get list of all disciplines.

        :return:
        """
        resp = await self.request_json(
            Methods.GET, DISCIPLINE, headers=self._headers
        )
        return [Discipline.model_validate(dsc) for dsc in resp]

    async def get_teachers(self) -> list[Teacher]:
        """
        Get teachers method.

        Get list of all teachers.

        :return:
        """
        resp = await self.request_json(
            Methods.GET, TEACHER, headers=self._headers
        )
        return [Teacher.model_validate(tch) for tch in resp]

    async def _get_id_by_title(
        self, title_tt: "TitleTimeTableType"
    ) -> "TimeTableType":
        """
        Get :code:`TimeTableType` from :code:`TitleTimeTableType`.

        :param title_tt: title time table object
        :raises CHSUApiLookupError: Group or Lecturer not found
        :return:
        """
        if isinstance(title_tt, Group):
            if title_tt.title in self._cache["groups"]:
                return self._cache["groups"][title_tt.title]
            groups = await self.get_student_groups()
            for g in groups:
                if g.title == title_tt.title:
                    group = GroupId(
                        id=g.id,
                        from_date=title_tt.from_date,
                        to_date=title_tt.to_date,
                    )
                    self._cache["groups"][title_tt.title] = group
                    return group
            msg = f"Group {title_tt.title} not found"
            raise CHSUApiLookupError(msg)

        if isinstance(title_tt, Lecturer):
            if title_tt.fullname in self._cache["lecturers"]:
                return self._cache["lecturers"][title_tt.fullname]
            teachers = await self.get_teachers()
            for t in teachers:
                if t.fio == title_tt.fullname:
                    lecturer = LecturerId(
                        id=t.id,
                        from_date=title_tt.from_date,
                        to_date=title_tt.to_date,
                    )
                    self._cache["lecturers"][title_tt.fullname] = lecturer
                    return lecturer
            msg = f"Lecturer {title_tt.fullname} not found"
            raise CHSUApiLookupError(msg)

        msg = f"Invalid time table type: {title_tt.__class__}"
        raise CHSUApiLookupError(msg)
