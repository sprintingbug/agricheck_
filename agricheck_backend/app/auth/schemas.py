from pydantic import BaseModel, EmailStr, field_validator

class RegisterIn(BaseModel):
    email: EmailStr
    password: str
    name: str
    security_question_1: str
    security_answer_1: str
    security_question_2: str
    security_answer_2: str
    security_question_3: str
    security_answer_3: str

    @field_validator('security_question_1', 'security_question_2', 'security_question_3')
    @classmethod
    def validate_security_questions(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('Security question cannot be empty')
        return v.strip()

    @field_validator('security_answer_1', 'security_answer_2', 'security_answer_3')
    @classmethod
    def validate_security_answers(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('Security answer cannot be empty')
        return v.strip()

class LoginIn(BaseModel):
    email: EmailStr
    password: str

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserOut(BaseModel):
    id: str
    email: EmailStr
    name: str
    role: str

class ForgetPasswordIn(BaseModel):
    email: EmailStr

class ForgetPasswordOut(BaseModel):
    message: str
    reset_token: str  # In production, this should be sent via email, not returned

class ResetPasswordIn(BaseModel):
    token: str
    new_password: str

class ResetPasswordOut(BaseModel):
    message: str

class ForgotPasswordSecurityQuestionsIn(BaseModel):
    email: EmailStr

class ForgotPasswordSecurityQuestionsOut(BaseModel):
    message: str
    questions: list[str]  # List of security questions for the user
    question_indices: list[int]  # List of question indices (0, 1, 2) corresponding to each question

class VerifySecurityAnswerIn(BaseModel):
    email: EmailStr
    question_index: int  # 0, 1, or 2 (which question they're answering)
    answer: str

class VerifySecurityAnswerOut(BaseModel):
    message: str
    verified: bool
    reset_token: str  # Token to use for password reset

class ResetPasswordSecurityQuestionsIn(BaseModel):
    email: EmailStr
    reset_token: str
    new_password: str

class ResetPasswordSecurityQuestionsOut(BaseModel):
    message: str

class UpdateProfileIn(BaseModel):
    name: str