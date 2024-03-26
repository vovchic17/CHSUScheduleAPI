from .base import CHSUResponseModel


class Faculty(CHSUResponseModel):
    """Faculty model"""

    id: int
    title: str


class Chair(CHSUResponseModel):
    """Cathedra model"""

    id: int
    title: str


class StudentGroup(CHSUResponseModel):
    id: int
    title: str
    course: int
    faculty: Faculty
    chair: Chair
