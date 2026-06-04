from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from app.models.pg_models import MaintenanceRequest, Lease, Property
from app.schemas.maintenance_schema import MaintenanceCreate, MaintenanceStatusUpdate

def raise_request(body: MaintenanceCreate, user_id: str, db: Session):
    lease = db.query(Lease).filter(Lease.id == body.lease_id, Lease.tenant_id == user_id).first()
    if not lease:
        raise HTTPException(404, "Lease not found for this user")
    if lease.status != "ACTIVE":
        raise HTTPException(400, "Lease must be ACTIVE")

    new_req = MaintenanceRequest(
        lease_id=body.lease_id,
        property_id=lease.property_id,
        tenant_id=user_id,
        title=body.title,
        category=body.category.upper(),
        priority=body.priority.upper(),
        description=body.description
    )
    db.add(new_req)
    db.commit()
    db.refresh(new_req)

    return {"message": "Maintenance request raised", "request": new_req}

def upload_images(request_id: str, urls: list, db: Session):
    req = db.query(MaintenanceRequest).filter(MaintenanceRequest.id == request_id).first()
    if req:
        # Assuming we append to existing if any, or overwrite
        # Let's overwrite / set to new list (comma separated string)
        req.image_urls = ",".join(urls)
        db.commit()
        db.refresh(req)
    return {"message": "Images uploaded", "request": req}

def list_requests(property_id: Optional[str], lease_id: Optional[str], status: Optional[str], user_id: str, roles: list, db: Session):
    query = db.query(MaintenanceRequest)

    if "SELLER" in roles or "ADMIN" in roles:
        query = query.join(Property, MaintenanceRequest.property_id == Property.id).filter(Property.owner_id == user_id)
    else:
        query = query.filter(MaintenanceRequest.tenant_id == user_id)

    if property_id:
        query = query.filter(MaintenanceRequest.property_id == property_id)
    if lease_id:
        query = query.filter(MaintenanceRequest.lease_id == lease_id)
    if status:
        query = query.filter(MaintenanceRequest.status == status.upper())

    query = query.order_by(MaintenanceRequest.created_at.desc())
    return query.all()

def get_request(request_id: str, db: Session):
    req = db.query(MaintenanceRequest).filter(MaintenanceRequest.id == request_id).first()
    if not req:
        raise HTTPException(404, "Maintenance request not found")
    return req

def update_status(request_id: str, body: MaintenanceStatusUpdate, db: Session):
    allowed = ("OPEN", "IN_PROGRESS", "RESOLVED", "CLOSED")
    if body.status.upper() not in allowed:
        raise HTTPException(400, f"Status must be one of: {allowed}")

    req = db.query(MaintenanceRequest).filter(MaintenanceRequest.id == request_id).first()
    if not req:
        raise HTTPException(404, "Maintenance request not found")

    req.status = body.status.upper()
    req.comment = body.comment
    db.commit()
    db.refresh(req)
    
    return {"message": f"Status updated to {body.status}", "request": req}

def check_request_exists(request_id: str, db: Session):
    return db.query(MaintenanceRequest).filter(MaintenanceRequest.id == request_id).first()

def delete_request(request_id: str, user_id: str, db: Session):
    req = db.query(MaintenanceRequest).filter(MaintenanceRequest.id == request_id).first()
    if not req:
        raise HTTPException(404, "Maintenance request not found")
    if str(req.tenant_id) != user_id:
        raise HTTPException(403, "You can only delete your own maintenance requests")
    
    db.delete(req)
    db.commit()
    return {"message": "Maintenance request deleted successfully"}
