from pydantic import BaseModel, EmailStr, field_validator

class RegisterBody(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    confirm_password: str

    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        return v

class LoginBody(BaseModel):
    email: EmailStr
    password: str
