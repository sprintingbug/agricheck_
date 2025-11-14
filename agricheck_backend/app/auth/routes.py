from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from app.db.session import get_db
from app.db.models import User
from app.auth.schemas import (
    RegisterIn, LoginIn, TokenOut, UserOut,
    ForgetPasswordIn, ForgetPasswordOut,
    ResetPasswordIn, ResetPasswordOut,
    ForgotPasswordSecurityQuestionsIn, ForgotPasswordSecurityQuestionsOut,
    VerifySecurityAnswerIn, VerifySecurityAnswerOut,
    ResetPasswordSecurityQuestionsIn, ResetPasswordSecurityQuestionsOut
)
from app.core.security import (
    hash_password, verify_password, create_access_token,
    hash_security_answer
)
from app.auth.password_reset import (
    get_security_questions_for_user,
    verify_user_security_answer,
    reset_user_password
)
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/register", response_model=UserOut, status_code=201)
def register(payload: RegisterIn, db: Session = Depends(get_db)):
    # Validate security questions are not empty
    if not payload.security_question_1 or not payload.security_question_1.strip():
        raise HTTPException(status_code=400, detail="Pakipili ang Security Question 1.")
    if not payload.security_question_2 or not payload.security_question_2.strip():
        raise HTTPException(status_code=400, detail="Pakipili ang Security Question 2.")
    if not payload.security_question_3 or not payload.security_question_3.strip():
        raise HTTPException(status_code=400, detail="Pakipili ang Security Question 3.")
    
    # Validate security answers are not empty
    if not payload.security_answer_1 or not payload.security_answer_1.strip():
        raise HTTPException(status_code=400, detail="Pakilagay ang sagot sa Security Question 1.")
    if not payload.security_answer_2 or not payload.security_answer_2.strip():
        raise HTTPException(status_code=400, detail="Pakilagay ang sagot sa Security Question 2.")
    if not payload.security_answer_3 or not payload.security_answer_3.strip():
        raise HTTPException(status_code=400, detail="Pakilagay ang sagot sa Security Question 3.")
    
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(status_code=400, detail="Ang email na ito ay nakarehistro na. Pakigamit ang ibang email.")
    user = User(
        email=payload.email,
        name=payload.name,
        password_hash=hash_password(payload.password),
        security_question_1=payload.security_question_1,
        security_answer_1=hash_security_answer(payload.security_answer_1),
        security_question_2=payload.security_question_2,
        security_answer_2=hash_security_answer(payload.security_answer_2),
        security_question_3=payload.security_question_3,
        security_answer_3=hash_security_answer(payload.security_answer_3),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return UserOut(id=user.id, email=user.email, name=user.name, role=user.role)

@router.post("/login", response_model=TokenOut)
def login(payload: LoginIn, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Maling email o password. Pakisubukang muli.")
    token = create_access_token(sub=user.id)
    return TokenOut(access_token=token)

@router.post("/forgot-password", response_model=ForgetPasswordOut, status_code=200)
def forgot_password(payload: ForgetPasswordIn, db: Session = Depends(get_db)):
    """Generate a password reset token for the user."""
    user = db.query(User).filter(User.email == payload.email).first()
    
    # Always return success to prevent email enumeration
    # In production, you would send the token via email instead of returning it
    reset_token = ""
    if user:
        reset_token = create_password_reset_token(user.email, expires_minutes=60)
        reset_token_expires = datetime.now(timezone.utc) + timedelta(minutes=60)
        
        user.reset_token = reset_token
        user.reset_token_expires = reset_token_expires
        db.commit()
    
    return ForgetPasswordOut(
        message="If an account with that email exists, a password reset token has been generated.",
        reset_token=reset_token  # In production, don't return this - send via email instead
    )

@router.post("/reset-password", response_model=ResetPasswordOut, status_code=200)
def reset_password(payload: ResetPasswordIn, db: Session = Depends(get_db)):
    """Reset password using a valid reset token."""
    # Verify the token
    email = verify_password_reset_token(payload.token)
    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Hindi valid o nag-expire na ang reset token. Pakisubukang muli."
        )
    
    # Find user by email
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hindi nahanap ang user. Pakisiguro na tama ang email."
        )
    
    # Verify token matches stored token and hasn't expired
    if user.reset_token != payload.token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Hindi valid ang reset token. Pakisubukang muli."
        )
    
    # Check token expiration - ensure both datetimes are timezone-aware
    if not user.reset_token_expires:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nag-expire na ang reset token. Pakisubukang muli."
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
            detail="Nag-expire na ang reset token. Pakisubukang muli."
        )
    
    # Update password and clear reset token
    user.password_hash = hash_password(payload.new_password)
    user.reset_token = None
    user.reset_token_expires = None
    db.commit()
    
    return ResetPasswordOut(message="Password has been reset successfully")

@router.post("/forgot-password-security-questions", response_model=ForgotPasswordSecurityQuestionsOut, status_code=200)
def forgot_password_security_questions(payload: ForgotPasswordSecurityQuestionsIn, db: Session = Depends(get_db)):
    """Get security questions for a user's email."""
    questions, question_indices = get_security_questions_for_user(payload.email, db)
    
    return ForgotPasswordSecurityQuestionsOut(
        message="If an account with that email exists, security questions are provided.",
        questions=questions,
        question_indices=question_indices
    )

@router.post("/verify-security-answer", response_model=VerifySecurityAnswerOut, status_code=200)
def verify_security_answer_endpoint(payload: VerifySecurityAnswerIn, db: Session = Depends(get_db)):
    """Verify a security answer and return a reset token if correct."""
    try:
        reset_token = verify_user_security_answer(
            email=payload.email,
            question_index=payload.question_index,
            answer=payload.answer,
            db=db
        )
        
        return VerifySecurityAnswerOut(
            message="Matagumpay na na-verify ang sagot!",
            verified=True,
            reset_token=reset_token
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error verifying security answer: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="May problema sa pag-verify ng sagot. Pakisubukang muli."
        )

@router.post("/reset-password-security-questions", response_model=ResetPasswordSecurityQuestionsOut, status_code=200)
def reset_password_security_questions(payload: ResetPasswordSecurityQuestionsIn, db: Session = Depends(get_db)):
    """Reset password using security question verification token."""
    try:
        reset_user_password(
            email=payload.email,
            reset_token=payload.reset_token,
            new_password=payload.new_password,
            db=db
        )
        
        return ResetPasswordSecurityQuestionsOut(message="Matagumpay na na-reset ang password!")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error resetting password for {payload.email}: {type(e).__name__}: {str(e)}", exc_info=True)
        # Check if it's a database-related error
        if "IntegrityError" in str(type(e).__name__) or "OperationalError" in str(type(e).__name__):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="May problema sa database. Pakisubukang muli."
            )
        # Return more informative error message
        error_detail = str(e) if str(e) else "May problema sa pag-reset ng password. Pakisubukang muli."
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_detail
        )
