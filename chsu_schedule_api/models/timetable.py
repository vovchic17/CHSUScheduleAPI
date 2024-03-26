from abc import abstractmethod
from datetime import datetime, timedelta, timezone

from pydantic import Field, validator

from chsu_schedule_api.models.building import Building
from chsu_schedule_api.models.discipline import Discipline
from chsu_schedule_api.models.teacher import Teacher

from .base import CHSUModel


class TimeTableType(CHSUModel):
    """Base time table model"""

    from_date: datetime
    to_date: datetime

    @property
    @abstractmethod
    def path(self) -> str:
        """Time table path"""


class Lecturer(TimeTableType):
    """Lecturer time table model"""

    id: int

    @property
    def path(self) -> str:
        """Time table path"""
        return (
            f"/from/{self.from_date.strftime('%d.%m.%Y')}/to/"
            f"{self.to_date.strftime('%d.%m.%Y')}/lecturerId/{self.id}"
        )


class Group(TimeTableType):
    """Group time table model"""

    id: int

    @property
    def path(self) -> str:
        """Timetable path"""
        return (
            f"/from/{self.from_date.strftime('%d.%m.%Y')}/to/"
            f"{self.to_date.strftime('%d.%m.%Y')}/groupId/{self.id}"
        )


class TTFull(TimeTableType):
    """Full time table model"""

    @property
    def path(self) -> str:
        """Timetable path"""
        return (
            f"/event/from/{self.from_date.strftime('%d.%m.%Y')}/to/"
            f"{self.to_date.strftime('%d.%m.%Y')}"
        )


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
