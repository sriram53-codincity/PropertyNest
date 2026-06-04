import json
from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from app.models.pg_models import SellerRequest, UserRole, Property
from app.models.mongo_models import PropertyDetails
from app.schemas.common_schema import StatusUpdate

async def create_seller_request(
    user_id: str,
    full_name: str,
    phone: str,
    address: str,
    property_title: str,
    property_address: str,
    property_type: str,
    monthly_rent: float,
    doc_type: str,
    declaration_accepted: bool,
    doc_url: str,
    image_urls: list,
    db: Session
):
    existing = db.query(SellerRequest).filter(
        SellerRequest.user_id == user_id, 
        SellerRequest.status == 'PENDING'
    ).first()
    
    if existing:
        raise HTTPException(400, "You already have a pending seller request")

    new_req = SellerRequest(
        user_id=user_id,
        full_name=full_name,
        phone=phone,
        address=address,
        property_title=property_title,
        property_address=property_address,
        property_type=property_type,
        monthly_rent=monthly_rent,
        doc_type=doc_type,
        doc_url=doc_url,
        image_urls=json.dumps(image_urls),
        declaration_accepted=declaration_accepted
    )
    db.add(new_req)
    db.commit()
    db.refresh(new_req)

    return {"message": "Seller request submitted", "request": new_req}

def get_my_requests(user_id: str, db: Session):
    return db.query(SellerRequest).filter(SellerRequest.user_id == user_id).order_by(SellerRequest.created_at.desc()).all()

def get_all_requests(status: Optional[str], db: Session):
    query = db.query(SellerRequest)
    if status:
        query = query.filter(SellerRequest.status == status.upper())
    return query.order_by(SellerRequest.created_at.desc()).all()

async def update_status(request_id: str, body: StatusUpdate, db: Session):
    if body.status not in ("APPROVED", "REJECTED"):
        raise HTTPException(400, "Status must be APPROVED or REJECTED")
    if body.status == "REJECTED" and not body.reason:
        raise HTTPException(400, "Reason is required when rejecting")

    req = db.query(SellerRequest).filter(SellerRequest.id == request_id).first()
    if not req:
        raise HTTPException(404, "Seller request not found")
    if req.status != "PENDING":
        raise HTTPException(400, "Only PENDING requests can be reviewed")

    if body.status == "APPROVED":
        # Add SELLER role if not exists
        existing_role = db.query(UserRole).filter(UserRole.user_id == req.user_id, UserRole.role == 'SELLER').first()
        if not existing_role:
            db.add(UserRole(user_id=req.user_id, role='SELLER'))

        # Create Property
        new_prop = Property(
            owner_id=req.user_id,
            title=req.property_title,
            city=req.property_address,
            property_type=req.property_type,
            monthly_rent=req.monthly_rent
        )
        db.add(new_prop)
        db.commit()
        db.refresh(new_prop)

        # Create MongoDB Details
        images = json.loads(req.image_urls) if req.image_urls else []
        detail = PropertyDetails(
            property_id=str(new_prop.id),
            description="",
            amenities=[],
            image_urls=images,
            inspection_reports=[]
        )
        await detail.insert()

        req.status = 'APPROVED'
        db.commit()

        return {"message": "Approved. User is now a SELLER and property created."}
    else:
        req.status = 'REJECTED'
        req.reason = body.reason
        db.commit()
        return {"message": "Rejected", "reason": body.reason}

def delete_request(request_id: str, user_id: str, db: Session):
    req = db.query(SellerRequest).filter(SellerRequest.id == request_id).first()
    if not req:
        raise HTTPException(404, "Seller request not found")
    if str(req.user_id) != user_id:
        raise HTTPException(403, "You can only delete your own requests")
    if req.status != "PENDING":
        raise HTTPException(400, "Only PENDING requests can be deleted")
    
    db.delete(req)
    db.commit()
    return {"message": "Seller request deleted successfully"}
