from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from sqlalchemy.orm import aliased
from dateutil.relativedelta import relativedelta
from app.models.pg_models import Lease, Application, Property, User
from app.schemas.lease_schema import LeaseCreate

async def create_lease(body: LeaseCreate, user_id: str, roles: list, db: AsyncSession):
    """
    Create a new lease for an approved rental application.
    
    Args:
        body (LeaseCreate): The lease creation details.
        user_id (str): The current user's ID.
        roles (list): The current user's roles.
        db (AsyncSession): The database session.
        
    Raises:
        HTTPException 404: If the application or property is not found.
        HTTPException 400: If the application is not approved or a lease already exists.
        HTTPException 403: If the user does not own the property.
        
    Returns:
        dict: A message and the newly created lease ID.
    """
    result = await db.execute(select(Application).filter(Application.id == int(body.application_id)))
    app = result.scalars().first()
    
    if not app:
        raise HTTPException(404, "Application not found")
    if app.status != "APPROVED":
        raise HTTPException(400, "Application must be APPROVED to create a lease")

    result = await db.execute(select(Property).filter(Property.id == app.property_id))
    prop = result.scalars().first()
    
    if not prop:
        raise HTTPException(404, "Property not found")
        
    if str(prop.owner_id) != user_id and "ADMIN" not in roles:
        raise HTTPException(403, "You do not own this property")

    result = await db.execute(select(Lease).filter(Lease.application_id == int(body.application_id)))
    existing_lease = result.scalars().first()
    if existing_lease:
        raise HTTPException(400, "A lease already exists for this application")

    start_date = app.move_in_date
    end_date   = start_date + relativedelta(months=int(app.lease_duration))

    new_lease = Lease(
        property_id=app.property_id,
        tenant_id=app.applicant_id,
        owner_id=prop.owner_id,
        application_id=int(body.application_id),
        start_date=start_date,
        end_date=end_date,
        monthly_rent=prop.monthly_rent
    )
    
    try:
        db.add(new_lease)
        prop.is_available = False
        await db.commit()
    except Exception:
        await db.rollback()
        raise
        
    await db.refresh(new_lease)
    return {"message": "Lease created successfully", "lease_id": str(new_lease.id)}


async def get_my_leases(user_id: str, db: AsyncSession):
    """
    Retrieve all leases where the user is either the tenant or the owner.
    
    Args:
        user_id (str): The current user's ID.
        db (AsyncSession): The database session.
        
    Returns:
        list: A list of lease details.
    """
    Tenant = aliased(User)
    Owner = aliased(User)

    query = select(
        Lease,
        Property.title.label("property_title"),
        Property.city,
        Tenant.full_name.label("tenant_name"),
        Tenant.email.label("tenant_email"),
        Owner.full_name.label("owner_name")
    ).join(Property, Lease.property_id == Property.id)\
     .join(Tenant, Lease.tenant_id == Tenant.id)\
     .join(Owner, Lease.owner_id == Owner.id)\
     .filter(or_(Lease.tenant_id == int(user_id), Lease.owner_id == int(user_id)))\
     .order_by(Lease.created_at.desc())

    result = await db.execute(query)
    results = result.all()

    leases = []
    for lease, property_title, city, tenant_name, tenant_email, owner_name in results:
        l_dict = lease.__dict__.copy()
        l_dict.pop('_sa_instance_state', None)
        l_dict.update({
            "property_title": property_title,
            "city": city,
            "tenant_name": tenant_name,
            "tenant_email": tenant_email,
            "owner_name": owner_name
        })
        leases.append(l_dict)
    
    return leases


async def get_lease(lease_id: str, user_id: str, roles: list, db: AsyncSession):
    """
    Retrieve the details of a single lease.
    
    Args:
        lease_id (str): The ID of the lease.
        user_id (str): The current user's ID.
        roles (list): The current user's roles.
        db (AsyncSession): The database session.
        
    Raises:
        HTTPException 404: If the lease is not found.
        HTTPException 403: If the user is neither the tenant nor the owner of the lease.
        
    Returns:
        dict: The lease details.
    """
    Tenant = aliased(User)
    Owner = aliased(User)

    query = select(
        Lease,
        Property.title.label("property_title"),
        Property.city,
        Tenant.full_name.label("tenant_name"),
        Tenant.email.label("tenant_email"),
        Owner.full_name.label("owner_name")
    ).join(Property, Lease.property_id == Property.id)\
     .join(Tenant, Lease.tenant_id == Tenant.id)\
     .join(Owner, Lease.owner_id == Owner.id)\
     .filter(Lease.id == int(lease_id))

    result = await db.execute(query)
    row = result.first()

    if not row:
        raise HTTPException(404, "Lease not found")

    lease, property_title, city, tenant_name, tenant_email, owner_name = row
    
    if str(lease.tenant_id) != user_id and str(lease.owner_id) != user_id and "ADMIN" not in roles:
        raise HTTPException(403, "You do not have access to this lease")

    l_dict = lease.__dict__.copy()
    l_dict.pop('_sa_instance_state', None)
    l_dict.update({
        "property_title": property_title,
        "city": city,
        "tenant_name": tenant_name,
        "tenant_email": tenant_email,
        "owner_name": owner_name
    })

    return l_dict
