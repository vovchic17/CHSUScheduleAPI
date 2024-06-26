from .base import CHSUResponseModel


class Discipline(CHSUResponseModel):
    """Discipline model."""

    id: int
    title: str

    def __str__(self) -> str:
        """Return a string representation of the discipline."""
        return f"<Discipline {self.title}>"
