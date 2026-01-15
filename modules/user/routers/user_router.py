from fastapi import APIRouter, Depends, HTTPException, status

from core.dependencies import get_user_service
from ..schemas.user_schema import UserResponseSchema, UserRequestSchema
UserRouter= APIRouter(
    prefix="/users",
    tags=["Users"]
)
# @UserRouter.post("/",response_model=UserResponseSchema)
# def create_user(
#         user: UserRequestSchema,
#         user_service = Depends(get_user_service)
# ):
#     try:
#         return user_service.create_user(user)
#     except ValueError as e:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail=str(e)
#         )
