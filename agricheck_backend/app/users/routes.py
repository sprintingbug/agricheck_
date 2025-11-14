# app/users/routes.py

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models import User, Scan
from app.core.security import decode_token
from app.auth.schemas import UserOut
from pydantic import BaseModel

class UpdateProfileIn(BaseModel):
    name: str

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
        raise HTTPException(status_code=401, detail="Hindi valid o nag-expire na ang token. Pakilagay muli ang inyong email at password.")

    # User.id is a UUID string, so use it directly
    user = db.query(User).filter(User.id == sub).first()
    if not user:
        raise HTTPException(status_code=401, detail="Hindi nahanap ang user. Pakilagay muli ang inyong email at password.")
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

@router.put("/me", response_model=UserOut)
def update_profile(
    payload: UpdateProfileIn,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> UserOut:
    """
    Update the authenticated user's profile.
    """
    current_user.name = payload.name
    db.commit()
    db.refresh(current_user)
    
    return UserOut(
        id=current_user.id,
        email=current_user.email,
        name=current_user.name,
        role=current_user.role,
    )

@router.get("/stats")
def get_user_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get statistics for the authenticated user (total scans, healthy crops, diseases, reports).
    """
    total_scans = db.query(Scan).filter(Scan.user_id == current_user.id).count()
    healthy_crops = db.query(Scan).filter(
        Scan.user_id == current_user.id,
        Scan.disease_name == "Healthy"
    ).count()
    diseases = db.query(Scan).filter(
        Scan.user_id == current_user.id,
        Scan.disease_name != "Healthy"
    ).count()
    reports = total_scans  # Reports = total scans for now
    
    return {
        "total_scans": total_scans,
        "healthy_crops": healthy_crops,
        "diseases": diseases,
        "reports": reports
    }
