from typing import List

from pydantic import BaseModel


class CategoryResponseSchema(BaseModel):
    id: int
    name: str
    description: str | None = None
    is_actived: bool

    class Config:
        from_attributes = True
class CategoryCreateSchema(BaseModel):
    name: str
    description: str | None = None
class CategoryUpdateSchema(BaseModel):
    name: str | None = None
    description: str | None = None
    is_actived: bool | None = None
