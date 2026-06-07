from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.database.connection import get_db
from app.auth import get_current_user, require_roles
from app.schemas.appointment_schema import AppointmentCreate
from app.schemas.common_schema import AppointmentStatusUpdate
from app.services import appointment_service

router = APIRouter(prefix="/api/appointments", tags=["Appointments"])

@router.post("/")
async def book_appointment(body: AppointmentCreate, current_user: dict = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    user_id = current_user["user_id"]
    return await appointment_service.book_appointment(body, user_id, db)


@router.get("/mine")
async def my_appointments(current_user: dict = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await appointment_service.get_my_appointments(current_user["user_id"], db)

@router.get("/for-owner")
async def owner_appointments(current_user: dict = Depends(require_roles("SELLER")), db: AsyncSession = Depends(get_db)):
    return await appointment_service.get_owner_appointments(current_user["user_id"], db)

@router.get("/")
async def all_appointments(
    status: Optional[str] = Query(None),
    current_user: dict = Depends(require_roles("ADMIN")),
    db: AsyncSession = Depends(get_db)
):
    return await appointment_service.get_all_appointments(status, db)


@router.patch("/{appointment_id}/status")
async def update_appointment_status(
    appointment_id: str,
    body: AppointmentStatusUpdate,
    current_user: dict = Depends(require_roles("ADMIN")),
    db: AsyncSession = Depends(get_db)
):
    return await appointment_service.update_appointment_status(appointment_id, body, db)

@router.delete("/{appointment_id}")
async def delete_appointment(
    appointment_id: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """USER: Cancel/delete your pending appointment."""
    return await appointment_service.delete_appointment(appointment_id, current_user["user_id"], db)
