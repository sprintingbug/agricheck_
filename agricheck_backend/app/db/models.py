from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime, Float, ForeignKey
from datetime import datetime, timezone
from typing import Optional
from app.db.session import Base
import uuid

def _uuid() -> str:
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=_uuid)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    name: Mapped[str] = mapped_column(String, default="")
    password_hash: Mapped[str] = mapped_column(String)
    role: Mapped[str] = mapped_column(String, default="user")
    reset_token: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    reset_token_expires: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    mobile_number: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    reset_code: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    reset_code_expires: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    # Security Questions (for password reset)
    security_question_1: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    security_answer_1: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    security_question_2: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    security_answer_2: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    security_question_3: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    security_answer_3: Mapped[Optional[str]] = mapped_column(String, nullable=True)

class Scan(Base):
    __tablename__ = "scans"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=_uuid)
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"), index=True)  # Foreign key to users.id
    image_path: Mapped[str] = mapped_column(String)  # Path to uploaded image
    disease_name: Mapped[str] = mapped_column(String)  # Detected disease name (e.g., "Healthy", "Leaf Blight")
    confidence: Mapped[float] = mapped_column(Float)  # Confidence score (0-100)
    recommendations: Mapped[Optional[str]] = mapped_column(String, nullable=True)  # Treatment recommendations
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
