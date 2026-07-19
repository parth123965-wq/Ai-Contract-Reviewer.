from fastapi import Depends , HTTPException , status
from fastapi.security import OAuth2PasswordBearer
from app.database.database import get_db
from sqlalchemy.orm import Session
from typing import Annotated
from app.auth.jwt import decode_access_token
from app.repositories.user_repository import UserRepository
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/token')

def get_current_user(token: Annotated[str,Depends(oauth2_scheme)], db: Annotated[Session,Depends(get_db)]) -> User:
    payload = decode_access_token(token=token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid authentication credentials'
        )
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid token payload'
        )
    user_repository = UserRepository()
    user = user_repository.get_user_by_id(db=db, user_id=user_id)
    if user is None:
        raise HTTPException(
            status_code=401,
            detail='User Not Found.'
        )
    return user