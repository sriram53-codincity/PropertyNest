from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from app.models.pg_models import Appointment, Property
from app.schemas.appointment_schema import AppointmentCreate
from app.schemas.common_schema import AppointmentStatusUpdate

def jitsi_url(appointment_id: str) -> str:
    return f"https://meet.jit.si/homelease-{appointment_id}"

async def book_appointment(body: AppointmentCreate, user_id: str, db: AsyncSession):
    owner_id = None
    if body.property_id:
        result = await db.execute(select(Property).filter(Property.id == body.property_id))
        prop = result.scalars().first()
        if prop:
            owner_id = prop.owner_id

    new_appt = Appointment(
        user_id=int(user_id),
        property_id=body.property_id,
        owner_id=owner_id,
        full_name=body.full_name,
        email=body.email,
        phone=body.phone,
        purpose=body.purpose,
        preferred_date=body.preferred_date,
        preferred_time=body.preferred_time,
        additional_notes=body.additional_notes
    )
    try:
        db.add(new_appt)
        await db.commit()
    except Exception:
        await db.rollback()
        raise
        
    await db.refresh(new_appt)
    
    return {"message": "Appointment booked! Admin will confirm shortly.", "appointment_id": str(new_appt.id)}

async def get_my_appointments(user_id: str, db: AsyncSession):
    result = await db.execute(select(Appointment).filter(Appointment.user_id == int(user_id)).order_by(Appointment.created_at.desc()))
    return result.scalars().all()

async def get_owner_appointments(owner_id: str, db: AsyncSession):
    result = await db.execute(select(Appointment).filter(Appointment.owner_id == int(owner_id)).order_by(Appointment.created_at.desc()))
    return result.scalars().all()

async def get_all_appointments(status: Optional[str], db: AsyncSession):
    query = select(Appointment)
    if status:
        query = query.filter(Appointment.status == status.upper())
    result = await db.execute(query.order_by(Appointment.created_at.desc()))
    return result.scalars().all()

async def update_appointment_status(appointment_id: str, body: AppointmentStatusUpdate, db: AsyncSession):
    if body.status not in ("CONFIRMED", "REJECTED", "COMPLETED", "CANCELLED"):
        raise HTTPException(400, "Invalid status")
    if body.status == "REJECTED" and not body.reason:
        raise HTTPException(400, "Reason required when rejecting")

    result = await db.execute(select(Appointment).filter(Appointment.id == int(appointment_id)))
    appt = result.scalars().first()
    if not appt:
        raise HTTPException(404, "Appointment not found")
    if appt.status != "PENDING":
        raise HTTPException(400, "Only PENDING appointments can be reviewed")

    meet_url = jitsi_url(appointment_id) if body.status == "CONFIRMED" else None

    appt.status = body.status
    appt.meet_url = meet_url
    appt.reason = body.reason
    
    try:
        await db.commit()
    except Exception:
        await db.rollback()
        raise
    
    msg = f"Confirmed! Join here: {meet_url}" if meet_url else "Rejected."
    return {"message": msg, "appointment_id": str(appt.id)}

async def delete_appointment(appointment_id: str, user_id: str, db: AsyncSession):
    result = await db.execute(select(Appointment).filter(Appointment.id == int(appointment_id)))
    appt = result.scalars().first()
    if not appt:
        raise HTTPException(404, "Appointment not found")
    if appt.user_id != int(user_id):
        raise HTTPException(403, "You can only delete your own appointments")
    if appt.status != "PENDING":
        raise HTTPException(400, "Only PENDING appointments can be deleted")
    
    try:
        await db.delete(appt)
        await db.commit()
    except Exception:
        await db.rollback()
        raise
        
    return {"message": "Appointment deleted successfully"}
