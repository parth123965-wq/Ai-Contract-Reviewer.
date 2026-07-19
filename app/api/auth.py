from fastapi import APIRouter , Depends
from app.database.database import get_db
from app.services.auth_service import AuthService , auth_service
from sqlalchemy.orm import Session
from typing import Annotated
from app.schemas.user import UserResponse , UserCreate , LoginResponse , UserLogin
from fastapi.security import OAuth2PasswordRequestForm

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
    
@auth_router.post('/login',response_model=LoginResponse)
def login(
    user: UserLogin,
    db: Annotated[Session,Depends(get_db)],
    service: Annotated[AuthService,Depends(auth_service)]
) -> LoginResponse:
    return service.login_user(
        db=db,
        user=user
    )
    
@auth_router.post('/token',response_model=LoginResponse)
def token(
    form_data: Annotated[OAuth2PasswordRequestForm,Depends()],
    db: Annotated[Session,Depends(get_db)],
    service: Annotated[AuthService,Depends(auth_service)]
) -> LoginResponse:
    user = UserLogin(
        email=form_data.username,
        password=form_data.password
    )
    return service.login_user(
        db=db,
        user=user
    )