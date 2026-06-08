from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.connection import get_db
from app.auth import get_current_user, require_roles
from app.schemas.lease_schema import LeaseCreate
from app.services import lease_service

router = APIRouter(prefix="/api/leases", tags=["Leases"])

@router.post("/")
async def create_lease(
    body: LeaseCreate,
    current_user: dict = Depends(require_roles("SELLER", "ADMIN")),
    db: AsyncSession = Depends(get_db)
):
    
    return await lease_service.create_lease(body, current_user["user_id"], current_user.get("roles", []), db)

@router.get("/me")
async def my_leases(current_user: dict = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    
    return await lease_service.get_my_leases(current_user["user_id"], db)

@router.get("/{lease_id}")
async def get_lease(lease_id: str, current_user: dict = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    
    return await lease_service.get_lease(
        lease_id, current_user["user_id"], current_user.get("roles", []), db
    )
