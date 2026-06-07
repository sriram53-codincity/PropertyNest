from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from typing import Optional
from app.models.pg_models import MaintenanceRequest, Lease, Property
from app.schemas.maintenance_schema import MaintenanceCreate, MaintenanceStatusUpdate

async def raise_request(body: MaintenanceCreate, user_id: str, db: AsyncSession):
    """
    Raise a new maintenance request for an active lease.
    
    Args:
        body (MaintenanceCreate): The maintenance request details.
        user_id (str): The ID of the tenant.
        db (AsyncSession): The database session.
        
    Raises:
        HTTPException 404: If the lease is not found.
        HTTPException 400: If the lease is not ACTIVE.
        
    Returns:
        dict: A success message and the new request ID.
    """
    result = await db.execute(select(Lease).filter(Lease.id == int(body.lease_id), Lease.tenant_id == int(user_id)))
    lease = result.scalars().first()
    if not lease:
        raise HTTPException(404, "Lease not found for this user")
    if lease.status != "ACTIVE":
        raise HTTPException(400, "Lease must be ACTIVE")

    new_req = MaintenanceRequest(
        lease_id=int(body.lease_id),
        property_id=lease.property_id,
        tenant_id=int(user_id),
        title=body.title,
        category=body.category.upper(),
        priority=body.priority.upper(),
        description=body.description,
        image_urls=[]
    )
    
    try:
        db.add(new_req)
        await db.commit()
    except Exception:
        await db.rollback()
        raise
        
    await db.refresh(new_req)
    return {"message": "Maintenance request raised", "request_id": str(new_req.id)}

async def upload_images(request_id: str, urls: list, db: AsyncSession):
    """
    Upload and attach images to an existing maintenance request.
    
    Args:
        request_id (str): The ID of the maintenance request.
        urls (list): List of image URLs.
        db (AsyncSession): The database session.
        
    Returns:
        dict: A success message and the request ID.
    """
    result = await db.execute(select(MaintenanceRequest).filter(MaintenanceRequest.id == int(request_id)))
    req = result.scalars().first()
    if req:
        req.image_urls = urls
        try:
            await db.commit()
            await db.refresh(req)
        except Exception:
            await db.rollback()
            raise
    return {"message": "Images uploaded", "request_id": str(req.id) if req else None}

async def list_requests(property_id: Optional[str], lease_id: Optional[str], status: Optional[str], as_admin: bool, user_id: str, roles: list, db: AsyncSession):
    """
    List maintenance requests based on filters and user roles.
    
    Args:
        property_id (Optional[str]): Filter by property ID.
        lease_id (Optional[str]): Filter by lease ID.
        status (Optional[str]): Filter by status.
        as_admin (bool): Whether to fetch as admin.
        user_id (str): The current user's ID.
        roles (list): The current user's roles.
        db (AsyncSession): The database session.
        
    Returns:
        list: A list of maintenance requests.
    """
    query = select(MaintenanceRequest)

    if as_admin and "ADMIN" in roles:
        pass # sees all
    elif "SELLER" in roles:
        query = query.join(Property, MaintenanceRequest.property_id == Property.id).filter(
            or_(Property.owner_id == int(user_id), MaintenanceRequest.tenant_id == int(user_id))
        )
    else:
        query = query.filter(MaintenanceRequest.tenant_id == int(user_id))

    if property_id:
        query = query.filter(MaintenanceRequest.property_id == int(property_id))
    if lease_id:
        query = query.filter(MaintenanceRequest.lease_id == int(lease_id))
    if status:
        query = query.filter(MaintenanceRequest.status == status.upper())

    query = query.order_by(MaintenanceRequest.created_at.desc())
    result = await db.execute(query)
    return result.scalars().all()

async def get_request(request_id: str, db: AsyncSession):
    """
    Retrieve a single maintenance request by its ID.
    
    Args:
        request_id (str): The maintenance request ID.
        db (AsyncSession): The database session.
        
    Raises:
        HTTPException 404: If the request is not found.
        
    Returns:
        MaintenanceRequest: The maintenance request object.
    """
    result = await db.execute(select(MaintenanceRequest).filter(MaintenanceRequest.id == int(request_id)))
    req = result.scalars().first()
    if not req:
        raise HTTPException(404, "Maintenance request not found")
    return req

async def update_status(request_id: str, body: MaintenanceStatusUpdate, db: AsyncSession):
    """
    Update the status and comments of a maintenance request.
    
    Args:
        request_id (str): The maintenance request ID.
        body (MaintenanceStatusUpdate): The status update details.
        db (AsyncSession): The database session.
        
    Raises:
        HTTPException 400: If the status is invalid.
        HTTPException 404: If the request is not found.
        
    Returns:
        dict: A success message and the request ID.
    """
    allowed = ("OPEN", "IN_PROGRESS", "RESOLVED", "CLOSED")
    if body.status.upper() not in allowed:
        raise HTTPException(400, f"Status must be one of: {allowed}")

    result = await db.execute(select(MaintenanceRequest).filter(MaintenanceRequest.id == int(request_id)))
    req = result.scalars().first()
    if not req:
        raise HTTPException(404, "Maintenance request not found")

    req.status = body.status.upper()
    req.comment = body.comment
    
    try:
        await db.commit()
        await db.refresh(req)
    except Exception:
        await db.rollback()
        raise
    
    return {"message": f"Status updated to {body.status}", "request_id": str(req.id)}

async def check_request_exists(request_id: str, db: AsyncSession):
    """
    Check if a maintenance request exists in the database.
    
    Args:
        request_id (str): The maintenance request ID.
        db (AsyncSession): The database session.
        
    Returns:
        MaintenanceRequest: The request if found, else None.
    """
    result = await db.execute(select(MaintenanceRequest).filter(MaintenanceRequest.id == int(request_id)))
    return result.scalars().first()

async def delete_request(request_id: str, user_id: str, db: AsyncSession):
    """
    Delete a maintenance request raised by the user.
    
    Args:
        request_id (str): The maintenance request ID.
        user_id (str): The tenant's user ID.
        db (AsyncSession): The database session.
        
    Raises:
        HTTPException 404: If the request is not found.
        HTTPException 403: If the user is not the tenant who raised it.
        
    Returns:
        dict: A success message.
    """
    result = await db.execute(select(MaintenanceRequest).filter(MaintenanceRequest.id == int(request_id)))
    req = result.scalars().first()
    if not req:
        raise HTTPException(404, "Maintenance request not found")
    if req.tenant_id != int(user_id):
        raise HTTPException(403, "You can only delete your own maintenance requests")
    
    try:
        await db.delete(req)
        await db.commit()
    except Exception:
        await db.rollback()
        raise
        
    return {"message": "Maintenance request deleted successfully"}
