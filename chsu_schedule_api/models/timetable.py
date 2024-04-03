from abc import abstractmethod
from datetime import datetime, timedelta, timezone

from pydantic import Field, validator

from chsu_schedule_api.models.building import Building
from chsu_schedule_api.models.discipline import Discipline
from chsu_schedule_api.models.teacher import Teacher

from .base import CHSUModel


class TimeTableType(CHSUModel):
    """Base time table model"""

    from_date: datetime | str
    to_date: datetime | str

    @property
    @abstractmethod
    def path(self) -> str:
        """Time table path"""

    def _dt_to_str(self) -> None:
        if isinstance(self.from_date, datetime):
            self.from_date = self.from_date.strftime("%d.%m.%Y")
        if isinstance(self.to_date, datetime):
            self.from_date = self.to_date.strftime("%d.%m.%Y")


class TitleTimeTableType(CHSUModel):
    """
    Base model for time tables
    that require pre id definition
    """

    from_date: datetime | str
    to_date: datetime | str


class LecturerId(TimeTableType):
    """Lecturer time table by id model"""

    id: int

    @property
    def path(self) -> str:
        """Time table path"""
        super()._dt_to_str()
        return f"/from/{self.from_date}/to/{self.to_date}/lecturerId/{self.id}"


class GroupId(TimeTableType):
    """Group time table by id model"""

    id: int

    @property
    def path(self) -> str:
        """Timetable path"""
        super()._dt_to_str()
        return f"/from/{self.from_date}/to/{self.to_date}/groupId/{self.id}"


class Full(TimeTableType):
    """Full time table model"""

    @property
    def path(self) -> str:
        """Timetable path"""
        super()._dt_to_str()
        return f"/event/from/{self.from_date}/to/{self.to_date}"


class Group(TitleTimeTableType):
    """Group time table by title model"""

    title: str


class Lecturer(TitleTimeTableType):
    """Lecturer time table by fullname model"""

    fullname: str


class TTStudentGroup(CHSUModel):
    id: int
    title: str


class TTAuditory(CHSUModel):
    id: int
    title: str


class TimeTable(CHSUModel):
    id: int
    date_event: datetime = Field(alias="dateEvent")
    start_time: str = Field(alias="startTime")
    end_time: str = Field(alias="endTime")
    discipline: Discipline
    groups: list[TTStudentGroup]
    build: Building | None
    auditory: TTAuditory
    lecturers: list[Teacher]  # can be empty
    abbrlessontype: str | None
    lessontype: str | None
    week: int
    weekday: int
    week_type: str = Field(alias="weekType")
    online_event: str | None = Field(alias="onlineEvent")
    online: int

    @validator("date_event", pre=True)
    @classmethod
    def validate_datetime(cls, value: str) -> datetime:
        """Validate datetime"""
        tz = timezone(timedelta(hours=3))
        return datetime.strptime(value, "%d.%m.%Y").replace(tzinfo=tz)
