from pydantic import Field

from .base import CHSUResponseModel


class Teacher(CHSUResponseModel):
    """Teacher model."""

    id: int
    last_name: str = Field(alias="lastName")
    first_name: str = Field(alias="firstName")
    middle_name: str | None = Field(alias="middleName")
    short_name: str = Field(alias="shortName")
    fio: str

    def __str__(self) -> str:
        """Return a string representation of the teacher."""
        return f"<Teacher {self.fio}>"
