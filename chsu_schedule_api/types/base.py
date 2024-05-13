from pydantic import BaseModel


class CHSUModel(BaseModel, extra="forbid"):
    """Base model for CHSU API."""


class CHSUResponseModel(CHSUModel):
    """Base model for CHSU API json responses."""
