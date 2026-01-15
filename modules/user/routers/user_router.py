from fastapi import APIRouter, Depends, HTTPException, status


UserRouter= APIRouter(
    prefix="/users",
    tags=["Users"]
)
