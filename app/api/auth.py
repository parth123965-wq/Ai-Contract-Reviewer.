from fastapi import APIRouter , Depends
from app.database.database import get_db
from app.auth.auth_service import AuthService , auth_service
from sqlalchemy.orm import Session
from typing import Annotated
from app.schemas.user import UserResponse , UserCreate

auth_router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@auth_router.post("/register", response_model=UserResponse,status_code=201)
def register_user(
    db: Annotated[Session,Depends(get_db)],
    auth_services: Annotated[AuthService,Depends(auth_service)],
    user: UserCreate
) -> UserResponse:
    return auth_services.register_user(
        db=db,
        user=user
    )