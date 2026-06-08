from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, asc
from typing import Optional
from app.models.pg_models import Property, User
from app.models.mongo_models import PropertyDetails
from beanie.operators import In
from app.schemas.property_schema import PropertyCreate, PropertyUpdate

def to_dict_prop(prop, mongo_detail: Optional[PropertyDetails], owner=None):
    d = {
        "id": str(prop.id),
        "owner_id": str(prop.owner_id),
        "owner_name": getattr(owner, "full_name", "Unknown"),
        "owner_email": getattr(owner, "email", "Unknown"),
        "title": prop.title,
        "city": prop.city,
        "property_type": prop.property_type,
        "bedrooms": prop.bedrooms,
        "bathrooms": prop.bathrooms,
        "monthly_rent": float(prop.monthly_rent),
        "status": prop.status,
        "is_available": prop.is_available,
        "reason": prop.reason,
        "created_at": prop.created_at,
    }
    if mongo_detail:
        d.update({
            "description": mongo_detail.description,
            "amenities": mongo_detail.amenities,
            "image_urls": mongo_detail.image_urls,
            "inspection_reports": mongo_detail.inspection_reports
        })
    else:
        d.update({"description": "", "amenities": [], "image_urls": [], "inspection_reports": []})
    return d

async def get_properties(
    db: AsyncSession,
    city: Optional[str] = None,
    property_type: Optional[str] = None,
    min_rent: Optional[float] = None,
    max_rent: Optional[float] = None,
    available: Optional[bool] = None,
    sort: str = "newest",
):
    query = select(Property).filter(Property.status == 'PUBLISHED')

    if city:
        query = query.filter(Property.city.ilike(city))
    if property_type:
        query = query.filter(Property.property_type == property_type.upper())
    if min_rent is not None:
        query = query.filter(Property.monthly_rent >= min_rent)
    if max_rent is not None:
        query = query.filter(Property.monthly_rent <= max_rent)
    if available is not None:
        query = query.filter(Property.is_available == available)

    if sort == "rent_asc":
        query = query.order_by(asc(Property.monthly_rent))
    elif sort == "rent_desc":
        query = query.order_by(desc(Property.monthly_rent))
    else:
        query = query.order_by(desc(Property.created_at))

    result = await db.execute(query)
    properties = result.scalars().all()
    if not properties:
        return []

    owner_ids = list(set(prop.owner_id for prop in properties))
    if owner_ids:
        res = await db.execute(select(User).filter(User.id.in_(owner_ids)))
        owners = res.scalars().all()
        owner_map = {owner.id: owner for owner in owners}
    else:
        owner_map = {}

    property_ids = [str(prop.id) for prop in properties]
    details = await PropertyDetails.find(In(PropertyDetails.property_id, property_ids)).to_list()
    details_map = {detail.property_id: detail for detail in details}

    out = []
    for prop in properties:
        detail = details_map.get(str(prop.id))
        owner = owner_map.get(prop.owner_id)
        out.append(to_dict_prop(prop, detail, owner))
    return out

async def get_my_properties(user_id: str, db: AsyncSession):
    result = await db.execute(select(Property).filter(Property.owner_id == int(user_id)).order_by(desc(Property.created_at)))
    properties = result.scalars().all()
    if not properties:
        return []
        
    owner_ids = list(set(prop.owner_id for prop in properties))
    if owner_ids:
        res = await db.execute(select(User).filter(User.id.in_(owner_ids)))
        owners = res.scalars().all()
        owner_map = {owner.id: owner for owner in owners}
    else:
        owner_map = {}

    property_ids = [str(prop.id) for prop in properties]
    details = await PropertyDetails.find(In(PropertyDetails.property_id, property_ids)).to_list()
    details_map = {detail.property_id: detail for detail in details}

    out = []
    for prop in properties:
        detail = details_map.get(str(prop.id))
        owner = owner_map.get(prop.owner_id)
        out.append(to_dict_prop(prop, detail, owner))
    return out

async def get_all_properties_admin(db: AsyncSession):
    result = await db.execute(select(Property).order_by(desc(Property.created_at)))
    properties = result.scalars().all()
    if not properties:
        return []
        
    owner_ids = list(set(prop.owner_id for prop in properties))
    if owner_ids:
        res = await db.execute(select(User).filter(User.id.in_(owner_ids)))
        owners = res.scalars().all()
        owner_map = {owner.id: owner for owner in owners}
    else:
        owner_map = {}

    property_ids = [str(prop.id) for prop in properties]
    details = await PropertyDetails.find(In(PropertyDetails.property_id, property_ids)).to_list()
    details_map = {detail.property_id: detail for detail in details}

    out = []
    for prop in properties:
        detail = details_map.get(str(prop.id))
        owner = owner_map.get(prop.owner_id)
        out.append(to_dict_prop(prop, detail, owner))
    return out

async def get_property(property_id: str, db: AsyncSession):
    result = await db.execute(select(Property).filter(Property.id == int(property_id)))
    prop = result.scalars().first()
    if not prop:
        raise HTTPException(404, "Property not found")

    detail = await PropertyDetails.find_one(PropertyDetails.property_id == str(prop.id))
    
    res = await db.execute(select(User).filter(User.id == prop.owner_id))
    owner = res.scalars().first()
    return to_dict_prop(prop, detail, owner)

async def create_property(body: PropertyCreate, user_id: str, db: AsyncSession):
    new_prop = Property(
        owner_id=int(user_id),
        title=body.title,
        city=body.city,
        property_type=body.property_type,
        bedrooms=body.bedrooms,
        bathrooms=body.bathrooms,
        monthly_rent=body.monthly_rent
    )
    try:
        db.add(new_prop)
        await db.commit()
    except Exception:
        await db.rollback()
        raise
        
    await db.refresh(new_prop)

    detail = PropertyDetails(
        property_id=str(new_prop.id),
        description=body.description or "",
        amenities=body.amenities or [],
        image_urls=[],
        inspection_reports=[]
    )
    await detail.insert()

    return {"message": "Property created (status: PENDING, awaiting admin approval)", "property_id": str(new_prop.id)}

async def update_property(property_id: str, body: PropertyUpdate, user_id: str, roles: list, db: AsyncSession):
    result = await db.execute(select(Property).filter(Property.id == int(property_id)))
    prop = result.scalars().first()
    if not prop:
        raise HTTPException(404, "Property not found")

    if str(prop.owner_id) != user_id and "ADMIN" not in roles:
        raise HTTPException(403, "You can only update your own properties")

    if body.title is not None: prop.title = body.title
    if body.city is not None: prop.city = body.city
    if body.property_type is not None: prop.property_type = body.property_type
    if body.bedrooms is not None: prop.bedrooms = body.bedrooms
    if body.bathrooms is not None: prop.bathrooms = body.bathrooms
    if body.monthly_rent is not None: prop.monthly_rent = body.monthly_rent
    if body.is_available is not None: prop.is_available = body.is_available

    if "ADMIN" in roles:
        if body.status == "REJECTED" and not body.reason:
            raise HTTPException(400, "Reason required when rejecting")
        if body.status:
            prop.status = body.status
        if body.reason:
            prop.reason = body.reason

    try:
        await db.commit()
        await db.refresh(prop)
    except Exception:
        await db.rollback()
        raise

    detail = await PropertyDetails.find_one(PropertyDetails.property_id == property_id)
    if not detail:
        detail = PropertyDetails(property_id=property_id)
        await detail.insert()

    if body.description is not None:
        detail.description = body.description
    if body.amenities is not None:
        detail.amenities = body.amenities
    
    await detail.save()

    return {"message": "Property updated", "property_id": str(prop.id)}

async def save_property_images(property_id: str, urls: list):
    detail = await PropertyDetails.find_one(PropertyDetails.property_id == property_id)
    if not detail:
        detail = PropertyDetails(property_id=property_id)
        await detail.insert()
    
    detail.image_urls.extend(urls)
    await detail.save()

async def delete_property(property_id: str, user_id: str, roles: list, db: AsyncSession):
    result = await db.execute(select(Property).filter(Property.id == int(property_id)))
    prop = result.scalars().first()
    if not prop:
        raise HTTPException(404, "Property not found")

    if str(prop.owner_id) != user_id and "ADMIN" not in roles:
        raise HTTPException(403, "You can only delete your own properties")

    try:
        await db.delete(prop)
        await db.commit()
    except Exception:
        await db.rollback()
        raise

    detail = await PropertyDetails.find_one(PropertyDetails.property_id == property_id)
    if detail:
        await detail.delete()

    return {"message": "Property deleted successfully"}
