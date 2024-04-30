from pydantic import Field

from .base import CHSUResponseModel


class Auditorium(CHSUResponseModel):
    id: int
    name: str
    number: str
    build_name: str = Field(alias="buildName")
    build_id: int = Field(alias="buildId")
    height: float
    length: float
    width: float

    def __str__(self) -> str:
        """Return a string representation of the auditorium"""
        return f"<Auditorium {self.build_name}>"
