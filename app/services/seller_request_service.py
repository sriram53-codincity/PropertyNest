from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from app.models.pg_models import SellerRequest, UserRole, Property
from app.models.mongo_models import PropertyDetails
from app.schemas.common_schema import SellerRequestStatusUpdate

async def create_seller_request(
    user_id: str,
    full_name: str,
    phone: str,
    address: str,
    property_title: str,
    property_address: str,
    district: str,
    property_type: str,
    bedrooms: int,
    monthly_rent: float,
    description: str,
    doc_type: str,
    declaration_accepted: bool,
    doc_url: str,
    image_urls: list,
    db: AsyncSession
):
    result = await db.execute(select(SellerRequest).filter(
        SellerRequest.user_id == int(user_id), 
        SellerRequest.status == 'PENDING'
    ))
    existing = result.scalars().first()
    
    if existing:
        raise HTTPException(400, "You already have a pending seller request")

    new_req = SellerRequest(
        user_id=int(user_id),
        full_name=full_name,
        phone=phone,
        address=address,
        property_title=property_title,
        property_address=property_address,
        district=district,
        property_type=property_type,
        bedrooms=bedrooms,
        monthly_rent=monthly_rent,
        description=description,
        doc_type=doc_type,
        doc_url=doc_url,
        image_urls=image_urls,
        declaration_accepted=declaration_accepted
    )
    
    try:
        db.add(new_req)
        await db.commit()
    except Exception:
        await db.rollback()
        raise
        
    await db.refresh(new_req)

    return {"message": "Seller request submitted", "request_id": str(new_req.id)}

async def get_my_requests(user_id: str, db: AsyncSession):
    result = await db.execute(select(SellerRequest).filter(SellerRequest.user_id == int(user_id)).order_by(SellerRequest.created_at.desc()))
    return result.scalars().all()

async def get_all_requests(status: Optional[str], db: AsyncSession):
    query = select(SellerRequest)
    if status:
        query = query.filter(SellerRequest.status == status.upper())
    result = await db.execute(query.order_by(SellerRequest.created_at.desc()))
    return result.scalars().all()

async def update_status(request_id: str, body: SellerRequestStatusUpdate, db: AsyncSession):
    if body.status not in ("APPROVED", "REJECTED"):
        raise HTTPException(400, "Status must be APPROVED or REJECTED")
    if body.status == "REJECTED" and not body.reason:
        raise HTTPException(400, "Reason is required when rejecting")

    result = await db.execute(select(SellerRequest).filter(SellerRequest.id == int(request_id)))
    req = result.scalars().first()
    if not req:
        raise HTTPException(404, "Seller request not found")
    if req.status != "PENDING":
        raise HTTPException(400, "Only PENDING requests can be reviewed")

    if body.status == "APPROVED":
        res_role = await db.execute(select(UserRole).filter(UserRole.user_id == req.user_id, UserRole.role == 'SELLER'))
        existing_role = res_role.scalars().first()
        
        try:
            if not existing_role:
                db.add(UserRole(user_id=req.user_id, role='SELLER'))

            new_prop = Property(
                owner_id=req.user_id,
                title=req.property_title,
                city=req.district,  # Use district as the city for correct extraction
                property_type=req.property_type,
                bedrooms=req.bedrooms,
                monthly_rent=req.monthly_rent,
                status='PUBLISHED',
                is_available=True
            )
            db.add(new_prop)
            await db.flush()
            
            req.status = 'APPROVED'
            
            images = req.image_urls or []
            detail = PropertyDetails(
                property_id=str(new_prop.id),
                description=req.description or "",
                amenities=[],
                image_urls=images,
                inspection_reports=[]
            )
            await detail.insert()
            await db.commit()
            
            return {"message": "Approved. User is now a SELLER and property created."}
        except Exception:
            await db.rollback()
            raise HTTPException(status_code=500, detail="Failed to create property details in MongoDB. Transaction rolled back.")
    else:
        req.status = 'REJECTED'
        req.reason = body.reason
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise
        return {"message": "Rejected", "reason": body.reason}

async def delete_request(request_id: str, user_id: str, db: AsyncSession):
    result = await db.execute(select(SellerRequest).filter(SellerRequest.id == int(request_id)))
    req = result.scalars().first()
    if not req:
        raise HTTPException(404, "Seller request not found")
    if req.user_id != int(user_id):
        raise HTTPException(403, "You can only delete your own requests")
    if req.status != "PENDING":
        raise HTTPException(400, "Only PENDING requests can be deleted")
    
    try:
        await db.delete(req)
        await db.commit()
    except Exception:
        await db.rollback()
        raise
        
    return {"message": "Seller request deleted successfully"}
