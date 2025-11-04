# app/users/routes.py

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models import User
from app.core.security import decode_token
from app.auth.schemas import UserOut

router = APIRouter(prefix="/users", tags=["users"])

# Used by Swagger's "Authorize" button and our dependency below.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """
    Resolve the current user from a Bearer JWT.
    Raises 401 if token invalid/expired or user not found.
    """
    sub = decode_token(token)
    if not sub:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    # User.id is a UUID string, so use it directly
    user = db.query(User).filter(User.id == sub).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


@router.get("/me", response_model=UserOut)
def me(current_user: User = Depends(get_current_user)) -> UserOut:
    """
    Return the authenticated user's public profile.
    """
    return UserOut(
        id=current_user.id,
        email=current_user.email,
        name=current_user.name,
        role=current_user.role,
    )
