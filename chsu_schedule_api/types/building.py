from .base import CHSUResponseModel


class Building(CHSUResponseModel):
    id: int
    title: str
    def __str__(self) -> str:
        """Return a string representation of the building."""
        return f"<Building {self.title}>"
