from .base import CHSUResponseModel


class Faculty(CHSUResponseModel):
    """Faculty model."""

    id: int
    title: str


class Chair(CHSUResponseModel):
    """Cathedra model."""

    id: int
    title: str


class StudentGroup(CHSUResponseModel):
    """StudentGroup model."""

    id: int
    title: str
    course: int
    faculty: Faculty
    chair: Chair

    def __str__(self) -> str:
        """Return a string representation of the group."""
        return f"<StudentGroup {self.title}>"
