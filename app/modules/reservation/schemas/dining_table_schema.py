from typing import Optional

from pydantic import BaseModel


class DiningTableResponse(BaseModel):
    id: int
    name: str
    capacity: int
    status: str

    class Config:
        from_attributes = True
class DiningTableCreate(BaseModel):
    name: str
    capacity: Optional[int] = 4