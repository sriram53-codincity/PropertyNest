from pydantic import BaseModel

class RegisterBody(BaseModel):
    full_name: str
    email: str
    password: str
    confirm_password: str

class LoginBody(BaseModel):
    email: str
    password: str
