from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from app.models.pg_models import Appointment
from app.schemas.appointment_schema import AppointmentCreate
from app.schemas.common_schema import StatusUpdate

def jitsi_url(appointment_id: str) -> str:
    return f"https://meet.jit.si/homelease-{appointment_id}"

def book_appointment(body: AppointmentCreate, user_id: Optional[str], db: Session):
    new_appt = Appointment(
        user_id=user_id,
        full_name=body.full_name,
        email=body.email,
        phone=body.phone,
        purpose=body.purpose,
        preferred_date=body.preferred_date,
        preferred_time=body.preferred_time,
        additional_notes=body.additional_notes
    )
    db.add(new_appt)
    db.commit()
    db.refresh(new_appt)
    
    return {"message": "Appointment booked! Admin will confirm shortly.", "appointment": new_appt}

def get_my_appointments(user_id: str, db: Session):
    return db.query(Appointment).filter(Appointment.user_id == user_id).order_by(Appointment.created_at.desc()).all()

def get_all_appointments(status: Optional[str], db: Session):
    query = db.query(Appointment)
    if status:
        query = query.filter(Appointment.status == status.upper())
    return query.order_by(Appointment.created_at.desc()).all()

def update_appointment_status(appointment_id: str, body: StatusUpdate, db: Session):
    if body.status not in ("CONFIRMED", "REJECTED"):
        raise HTTPException(400, "Status must be CONFIRMED or REJECTED")
    if body.status == "REJECTED" and not body.reason:
        raise HTTPException(400, "Reason required when rejecting")

    appt = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appt:
        raise HTTPException(404, "Appointment not found")
    if appt.status != "PENDING":
        raise HTTPException(400, "Only PENDING appointments can be reviewed")

    meet_url = jitsi_url(appointment_id) if body.status == "CONFIRMED" else None

    appt.status = body.status
    appt.meet_url = meet_url
    appt.reason = body.reason
    db.commit()
    db.refresh(appt)

    msg = f"Confirmed! Join here: {meet_url}" if meet_url else "Rejected."
    return {"message": msg, "appointment": appt}

def delete_appointment(appointment_id: str, user_id: str, db: Session):
    appt = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appt:
        raise HTTPException(404, "Appointment not found")
    if str(appt.user_id) != user_id:
        raise HTTPException(403, "You can only delete your own appointments")
    if appt.status != "PENDING":
        raise HTTPException(400, "Only PENDING appointments can be deleted")
    
    db.delete(appt)
    db.commit()
    return {"message": "Appointment deleted successfully"}
