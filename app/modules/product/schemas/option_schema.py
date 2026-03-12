from pydantic import BaseModel


class OptionResponseSchema(BaseModel):
    id: int
    name: str
    min_select: int
    max_select: int
    is_active: bool
    class Config:
        from_attributes = True
class OptionCreateSchema(BaseModel):
    name: str
    min_select: int
    max_select: int
class OptionUpdateSchema(BaseModel):
    name: str | None = None
    min_select: int
    max_select: int
    is_active: bool
