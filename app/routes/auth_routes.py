from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.auth import get_current_user
from app.schemas.auth_schema import RegisterBody, LoginBody
from app.services import auth_service

router = APIRouter(prefix="/api/auth", tags=["Auth"])

@router.post("/register")
def register(body: RegisterBody, db: Session = Depends(get_db)):
    return auth_service.register_user(body, db)

@router.post("/login")
def login(body: LoginBody, db: Session = Depends(get_db)):
    return auth_service.login_user(body, db)

@router.get("/me")
def get_me(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    return auth_service.get_current_user_profile(current_user["user_id"], db)
