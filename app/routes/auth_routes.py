from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.connection import get_db
from app.auth import get_current_user, require_roles
from app.schemas.auth_schema import RegisterBody, LoginBody
from app.services import auth_service

router = APIRouter(prefix="/api/auth", tags=["Auth"])

@router.post("/register")
async def register(body: RegisterBody, db: AsyncSession = Depends(get_db)):
    return await auth_service.register_user(body, db)

@router.post("/login")
async def login(body: LoginBody, db: AsyncSession = Depends(get_db)):
    return await auth_service.login_user(body, db)

@router.get("/me")
async def get_me(current_user: dict = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await auth_service.get_current_user_profile(current_user["user_id"], db)

@router.get("/users")
async def get_all_users(current_user: dict = Depends(require_roles("ADMIN")), db: AsyncSession = Depends(get_db)):
    return await auth_service.get_all_users_admin(db)

@router.delete("/users/{user_id}")
async def delete_user(user_id: str, current_user: dict = Depends(require_roles("ADMIN")), db: AsyncSession = Depends(get_db)):
    return await auth_service.delete_user_admin(user_id, db)
