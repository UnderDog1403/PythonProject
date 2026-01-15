from pydantic import BaseModel
from uuid import UUID

class UserResponseSchema(BaseModel):
    id: UUID
    name: str
    email: str
    address: str | None = None
    image: str | None = None
    class Config:
        from_attributes = True