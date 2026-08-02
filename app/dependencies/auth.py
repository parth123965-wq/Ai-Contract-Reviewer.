"""
=========================================================
AUTH DEPENDENCIES

Responsibilities:
- Extract JWT from HttpOnly cookie
- Validate JWT token
- Fetch current authenticated user
- Protect private routes

Cookie:
- ai_contract_session
=========================================================
"""


from fastapi import Depends, HTTPException, status, Request
from app.database.database import get_db
from sqlalchemy.orm import Session
from typing import Annotated

from app.auth.jwt import decode_access_token
from app.repositories.user_repository import UserRepository
from app.models.user import User



# =======================================================
# SECTION 1: CURRENT USER DEPENDENCY
# =======================================================


def get_current_user(
    request: Request,
    db: Annotated[Session, Depends(get_db)]
) -> User:


    # ---------------------------------------------------
    # Extract JWT from HttpOnly Cookie
    # ---------------------------------------------------

    token = request.cookies.get(
        "ai_contract_session"
    )


    if token is None:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )


    # ---------------------------------------------------
    # Decode JWT
    # ---------------------------------------------------

    payload = decode_access_token(
        token=token
    )


    if payload is None:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )


    # ---------------------------------------------------
    # Extract User ID
    # ---------------------------------------------------

    user_id = payload.get("sub")


    if user_id is None:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )


    # ---------------------------------------------------
    # Fetch User
    # ---------------------------------------------------

    user_repository = UserRepository()


    user = user_repository.get_user_by_id(
        db=db,
        user_id=user_id
    )


    if user is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )


    return user