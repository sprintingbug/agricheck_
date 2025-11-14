"""
Password Reset Flow - Security Questions Based
Clean implementation for password reset functionality
"""
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from app.db.models import User
from app.core.security import (
    hash_password,
    verify_security_answer,
    create_password_reset_token,
    verify_password_reset_token
)
import logging
from typing import List, Tuple

logger = logging.getLogger(__name__)

def get_security_questions_for_user(email: str, db: Session) -> Tuple[List[str], List[int]]:
    """
    Get security questions for a user.
    
    Returns:
        (questions, indices) - Lists of questions and their indices (0, 1, 2)
    """
    user = db.query(User).filter(User.email == email).first()
    
    questions = []
    indices = []
    
    if user:
        if user.security_question_1:
            questions.append(user.security_question_1)
            indices.append(0)
        if user.security_question_2:
            questions.append(user.security_question_2)
            indices.append(1)
        if user.security_question_3:
            questions.append(user.security_question_3)
            indices.append(2)
    
    return questions, indices

def verify_user_security_answer(
    email: str,
    question_index: int,
    answer: str,
    db: Session
) -> str:
    """
    Verify a user's security answer and generate reset token.
    
    Args:
        email: User email
        question_index: Question index (0, 1, or 2)
        answer: User's answer
        db: Database session
    
    Returns:
        Reset token string
    
    Raises:
        HTTPException if verification fails
    """
    user = db.query(User).filter(User.email == email).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hindi nahanap ang user. Pakisiguro na tama ang email."
        )
    
    # Get the correct security answer based on question_index
    if question_index == 0:
        if not user.security_question_1 or not user.security_answer_1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Hindi nahanap ang security question. Pakisubukang muli."
            )
        is_correct = verify_security_answer(answer, user.security_answer_1)
    elif question_index == 1:
        if not user.security_question_2 or not user.security_answer_2:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Hindi nahanap ang security question. Pakisubukang muli."
            )
        is_correct = verify_security_answer(answer, user.security_answer_2)
    elif question_index == 2:
        if not user.security_question_3 or not user.security_answer_3:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Hindi nahanap ang security question. Pakisubukang muli."
            )
        is_correct = verify_security_answer(answer, user.security_answer_3)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Hindi valid ang question index. Dapat ay 0, 1, o 2."
        )
    
    if not is_correct:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Maling sagot. Pakisubukang muli."
        )
    
    # Generate reset token
    reset_token = create_password_reset_token(email, expires_minutes=30)
    reset_token_expires = datetime.now(timezone.utc) + timedelta(minutes=30)
    
    # Store token in database
    user.reset_token = reset_token
    user.reset_token_expires = reset_token_expires
    db.commit()
    
    logger.info(f"Security answer verified for user: {email}, reset token generated")
    
    return reset_token

def reset_user_password(
    email: str,
    reset_token: str,
    new_password: str,
    db: Session
) -> None:
    """
    Reset user password using valid reset token.
    
    Args:
        email: User email
        reset_token: Reset token from security answer verification
        new_password: New password
        db: Database session
    
    Raises:
        HTTPException if reset fails
    """
    # Validate new password
    if not new_password or not new_password.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ang password ay hindi dapat walang laman."
        )
    
    if len(new_password.strip()) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ang password ay dapat hindi bababa sa 8 characters."
        )
    
    # Find user by email
    user = db.query(User).filter(User.email == email).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hindi nahanap ang user. Pakisiguro na tama ang email."
        )
    
    # Verify token matches stored token
    if not user.reset_token or user.reset_token != reset_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Hindi valid ang reset token. Pakisubukang muli o mag-verify muli ng security answer."
        )
    
    # Check token expiration - ensure both datetimes are timezone-aware
    if not user.reset_token_expires:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nag-expire na ang reset token. Pakisubukang muli o mag-verify muli ng security answer."
        )
    
    # Ensure reset_token_expires is timezone-aware for comparison
    now = datetime.now(timezone.utc)
    expires = user.reset_token_expires
    
    # If expires is naive, make it timezone-aware (assume UTC)
    if expires.tzinfo is None:
        expires = expires.replace(tzinfo=timezone.utc)
    
    if expires < now:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nag-expire na ang reset token. Pakisubukang muli o mag-verify muli ng security answer."
        )
    
    # Verify token from JWT (additional validation)
    email_from_token = verify_password_reset_token(reset_token)
    if not email_from_token or email_from_token != email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Hindi valid o nag-expire na ang reset token. Pakisubukang muli."
        )
    
    # Update password and clear reset token
    try:
        user.password_hash = hash_password(new_password)
        user.reset_token = None
        user.reset_token_expires = None
        db.commit()
        db.refresh(user)  # Refresh to ensure changes are saved
        logger.info(f"Password reset successful for user: {email}")
    except Exception as e:
        db.rollback()  # Rollback on error
        logger.error(f"Error updating password for user {email}: {type(e).__name__}: {str(e)}", exc_info=True)
        # Don't expose internal error details to user, but log them
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="May problema sa pag-update ng password. Pakisubukang muli."
        )

