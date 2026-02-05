from pydantic import BaseModel
from uuid import UUID

class UserResponseSchema(BaseModel):
    id: UUID
    name: str
    email: str
    address: str | None = None
    image: str | None = None
    phone: str | None = None
    is_active: bool
    is_verified: bool
    class Config:
        from_attributes = True

class UserListResponseSchema(BaseModel):
    users: list[UserResponseSchema]
    total: int
    total_pages: int
    page: int
    limit: int
class UserUpdateSchema(BaseModel):
    name: str | None = None
    address: str | None = None
    image: str | None = None
    phone: str | None = None
class UserUpdateActiveSchema(BaseModel):
    is_active: bool