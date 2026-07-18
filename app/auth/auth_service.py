from sqlalchemy.orm import Session
from app.auth.password import hash_password
from app.schemas.user import UserCreate
from app.models.user import User
from app.repositories.user_repository import UserRepository
from fastapi import HTTPException

class AuthService:
    
    def __init__(self):
        self.user_repository = UserRepository()
        
    def register_user(self, db:Session, user: UserCreate) -> User:
        existing_user = self.user_repository.get_user_by_email(db=db, email=user.email)
        if existing_user is not None:
            raise HTTPException(
                status_code=400,
                detail='Email already registered'
            )
        hashed_password = hash_password(password=user.password)
        new_user = User(
            username = user.username,
            email = user.email,
            password_hash = hashed_password
        )
        saved_user = self.user_repository.create_user(
            db=db,
            user=new_user
        )
        return saved_user
    
def auth_service() -> AuthService:
    return AuthService() 