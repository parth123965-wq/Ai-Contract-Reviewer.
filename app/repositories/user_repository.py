from sqlalchemy.orm import Session
from app.models.user import User
from sqlalchemy import select 
from typing import Optional

class UserRepository:
    def create_user(self, db: Session, user: User) -> User:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def get_user_by_email(self, db: Session, email: str) -> Optional[User]:
        statement = select(User).where(User.email == email)
        result = db.execute(statement=statement).scalar_one_or_none()
        return result
        
    def get_user_by_id(self, db: Session, user_id: int) -> Optional[User]:
        statement = select(User).where(User.id == user_id)
        result = db.execute(statement=statement).scalar_one_or_none()
        return result