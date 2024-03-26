from .auditorium import Auditorium
from .base import CHSUModel, CHSUResponseModel
from .building import Building
from .department import Department, Node
from .discipline import Discipline
from .student_group import Chair, Faculty, StudentGroup
from .teacher import Teacher
from .timetable import (
    Group,
    Lecturer,
    TimeTable,
    TimeTableType,
    TTAuditory,
    TTFull,
    TTStudentGroup,
)

__all__ = (
    "Auditorium",
    "CHSUModel",
    "CHSUResponseModel",
    "Building",
    "Department",
    "Node",
    "Discipline",
    "Chair",
    "Faculty",
    "StudentGroup",
    "Teacher",
    "Group",
    "Lecturer",
    "TimeTable",
    "TimeTableType",
    "TTAuditory",
    "TTFull",
    "TTStudentGroup",
)
