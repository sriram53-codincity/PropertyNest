from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional
from app.models.pg_models import Application, Property
from app.schemas.application_schema import ApplicationCreate
from app.schemas.common_schema import StatusUpdate

def submit_application(body: ApplicationCreate, user_id: str, db: Session):
    prop = db.query(Property).filter(Property.id == body.property_id).first()
    if not prop:
        raise HTTPException(404, "Property not found")
    if prop.status != "PUBLISHED":
        raise HTTPException(400, "Property is not accepting applications")
    if not prop.is_available:
        raise HTTPException(400, "Property is not available")

    existing = db.query(Application).filter(
        Application.property_id == body.property_id,
        Application.applicant_id == user_id,
        Application.status == 'PENDING'
    ).first()
    
    if existing:
        raise HTTPException(400, "You already applied for this property")

    new_app = Application(
        property_id=body.property_id,
        applicant_id=user_id,
        full_name=body.full_name,
        email=body.email,
        phone=body.phone,
        date_of_birth=body.date_of_birth,
        marital_status=body.marital_status,
        employment_type=body.employment_type,
        college_name=body.college_name,
        company_name=body.company_name,
        monthly_income=body.monthly_income,
        current_address=body.current_address,
        move_in_date=body.move_in_date,
        lease_duration=body.lease_duration,
        num_occupants=body.num_occupants,
        additional_notes=body.additional_notes
    )
    db.add(new_app)
    db.commit()
    db.refresh(new_app)
    
    # We must convert to dict or let FastAPI handle the SQLAlchemy model directly.
    # FastAPI can return SQLAlchemy models directly if we use `response_model` or just return the object.
    return {"message": "Application submitted", "application": new_app}

def list_applications(property_id: Optional[str], user_id: str, roles: list, db: Session):
    query = db.query(Application)

    if "SELLER" in roles or "ADMIN" in roles:
        if property_id:
            query = query.filter(Application.property_id == property_id)
        else:
            query = query.join(Property, Application.property_id == Property.id).filter(Property.owner_id == user_id)
    else:
        query = query.filter(Application.applicant_id == user_id)

    query = query.order_by(Application.created_at.desc())
    return query.all()

def get_application(application_id: str, db: Session):
    app = db.query(Application).filter(Application.id == application_id).first()
    if not app:
        raise HTTPException(404, "Application not found")
    return app

def update_application_status(application_id: str, body: StatusUpdate, db: Session):
    if body.status not in ("APPROVED", "REJECTED"):
        raise HTTPException(400, "Status must be APPROVED or REJECTED")
    if body.status == "REJECTED" and not body.reason:
        raise HTTPException(400, "Reason required when rejecting")

    app = db.query(Application).filter(Application.id == application_id).first()
    if not app:
        raise HTTPException(404, "Application not found")
    if app.status != "PENDING":
        raise HTTPException(400, "Only PENDING applications can be reviewed")

    if body.status == "APPROVED":
        app.status = "APPROVED"
        
        other_apps = db.query(Application).filter(
            Application.property_id == app.property_id,
            Application.status == 'PENDING',
            Application.id != application_id
        ).all()
        for other in other_apps:
            other.status = "REJECTED"
            other.reason = "Another applicant was selected"

        db.commit()
        return {"message": "Application approved. You can now create a lease for it."}
    else:
        app.status = "REJECTED"
        app.reason = body.reason
        db.commit()
        return {"message": "Application rejected", "reason": body.reason}

def delete_application(application_id: str, user_id: str, db: Session):
    app = db.query(Application).filter(Application.id == application_id).first()
    if not app:
        raise HTTPException(404, "Application not found")
    if str(app.applicant_id) != user_id:
        raise HTTPException(403, "You can only delete your own applications")
    if app.status != "PENDING":
        raise HTTPException(400, "Only PENDING applications can be deleted")
    
    db.delete(app)
    db.commit()
    return {"message": "Application deleted successfully"}
