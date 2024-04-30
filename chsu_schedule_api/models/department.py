from pydantic import Field

from .base import CHSUResponseModel


class Node(CHSUResponseModel):
    id: int
    parent_id: int = Field(alias="parentId")
    title: str
    short_title: str = Field(alias="shortTitle")
    type_code: str = Field(alias="typeCode")
    type_title: str = Field(alias="typeTitle")


class Department(CHSUResponseModel):
    node: Node
    items: list["Department"]

    def __str__(self) -> str:
        """Return a string representation of the building"""
        return f"<Department {self.node.title}>"
