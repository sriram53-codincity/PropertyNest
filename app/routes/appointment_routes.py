from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.database.connection import get_db
from app.auth import get_current_user, require_roles
from app.schemas.appointment_schema import AppointmentCreate
from app.schemas.common_schema import StatusUpdate
from app.services import appointment_service

router = APIRouter(prefix="/api/appointments", tags=["Appointments"])

@router.post("/")
def book_appointment(body: AppointmentCreate, current_user: Optional[dict] = Depends(get_current_user), db: Session = Depends(get_db)):
    user_id = current_user["user_id"] if current_user else None
    return appointment_service.book_appointment(body, user_id, db)


@router.get("/mine")
def my_appointments(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    return appointment_service.get_my_appointments(current_user["user_id"], db)


@router.get("/")
def all_appointments(
    status: Optional[str] = Query(None),
    current_user: dict = Depends(require_roles("ADMIN")),
    db: Session = Depends(get_db)
):
    return appointment_service.get_all_appointments(status, db)


@router.patch("/{appointment_id}/status")
def update_appointment_status(
    appointment_id: str,
    body: StatusUpdate,
    current_user: dict = Depends(require_roles("ADMIN")),
    db: Session = Depends(get_db)
):
    return appointment_service.update_appointment_status(appointment_id, body, db)

@router.delete("/{appointment_id}")
def delete_appointment(
    appointment_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """USER: Cancel/delete your pending appointment."""
    return appointment_service.delete_appointment(appointment_id, current_user["user_id"], db)
