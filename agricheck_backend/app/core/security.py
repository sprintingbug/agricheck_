from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt, JWTError
import bcrypt
from app.core.config import settings

ALGORITHM = "HS256"

def _truncate_password(password: str) -> bytes:
    """Truncate password to 72 bytes as required by bcrypt."""
    password_bytes = password.encode('utf-8')
    if len(password_bytes) > 72:
        # Truncate to 72 bytes
        return password_bytes[:72]
    return password_bytes

def hash_password(password: str) -> str:
    """Hash a password using bcrypt. Automatically truncates to 72 bytes."""
    password_bytes = _truncate_password(password)
    # Generate salt and hash
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    """Verify a password against a bcrypt hash. Automatically truncates to 72 bytes."""
    password_bytes = _truncate_password(password)
    hashed_bytes = hashed.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)

def hash_security_answer(answer: str) -> str:
    """Hash a security answer for storage (case-insensitive comparison)."""
    # Normalize to lowercase for case-insensitive comparison
    normalized = answer.lower().strip()
    return hash_password(normalized)

def verify_security_answer(answer: str, hashed: str) -> bool:
    """Verify a security answer (case-insensitive)."""
    # Normalize to lowercase for case-insensitive comparison
    normalized = answer.lower().strip()
    return verify_password(normalized, hashed)

def create_access_token(sub: str, expires_minutes: Optional[int] = None) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=expires_minutes or settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    payload = {"sub": sub, "exp": expire}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> Optional[str]:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None

def create_password_reset_token(email: str, expires_minutes: int = 60) -> str:
    """Create a password reset token that expires in specified minutes."""
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
    payload = {"sub": email, "exp": expire, "type": "password_reset"}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=ALGORITHM)

def verify_password_reset_token(token: str) -> Optional[str]:
    """Verify a password reset token and return the email if valid."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "password_reset":
            return None
        return payload.get("sub")
    except JWTError:
        return None

