from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from app.models.pg_models import Application, Property, User
from app.schemas.application_schema import ApplicationCreate
from app.schemas.common_schema import ApplicationStatusUpdate

async def create_application(body: ApplicationCreate, user_id: str, db: AsyncSession):
    """
    Submit a rental application for a property.
    
    Args:
        body (ApplicationCreate): The application details.
        user_id (str): The applicant's user ID.
        db (AsyncSession): The database session.
        
    Raises:
        HTTPException 404: If the property is not found.
        HTTPException 400: If the property is not available or if already applied.
        
    Returns:
        dict: A message and the application ID.
    """
    
    result = await db.execute(select(Property).filter(Property.id == int(body.property_id)))
    prop = result.scalars().first()
    
    if not prop:
        raise HTTPException(404, "Property not found")
    if prop.status != "PUBLISHED":
        raise HTTPException(400, "Property is not accepting applications")
    if not prop.is_available:
        raise HTTPException(400, "Property is not available")

    result = await db.execute(select(Application).filter(
        Application.property_id == int(body.property_id),
        Application.applicant_id == int(user_id),
        Application.status == 'PENDING'
    ))
    existing = result.scalars().first()
    
    if existing:
        raise HTTPException(400, "You already applied for this property")

    new_app = Application(
        property_id=int(body.property_id),
        applicant_id=int(user_id),
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
    
    try:
        db.add(new_app)
        await db.commit()
    except Exception:
        await db.rollback()
        raise

    await db.refresh(new_app)
    return {"message": "Application submitted", "application_id": str(new_app.id)}

async def get_applications(user_id: str, roles: list, db: AsyncSession):
    """
    List applications relevant to the current user.
    If the user has SELLER role, lists applications for their properties as well as their own applications.
    Otherwise, lists only their own applications.
    
    Args:
        user_id (str): The user ID.
        roles (list): The user's roles.
        db (AsyncSession): The database session.
        
    Returns:
        list: A list of applications with property titles.
    """
    query = select(Application, Property.title.label("property_title"), User.full_name.label("owner_name"))\
        .join(Property, Application.property_id == Property.id)\
        .join(User, Property.owner_id == User.id)

    if "SELLER" in roles:
        query = query.filter(
            or_(Property.owner_id == int(user_id), Application.applicant_id == int(user_id))
        )
    else:
        query = query.filter(Application.applicant_id == int(user_id))

    query = query.order_by(Application.created_at.desc())
    result = await db.execute(query)
    results = result.all()

    apps = []
    for app, prop_title, owner_name in results:
        app_dict = app.__dict__.copy()
        app_dict.pop('_sa_instance_state', None)
        app_dict["property_title"] = prop_title
        app_dict["owner_name"] = owner_name
        apps.append(app_dict)
    
    return apps

async def get_application(application_id: str, db: AsyncSession):
    """
    Retrieve details of a single rental application.
    
    Args:
        application_id (str): The application ID.
        db (AsyncSession): The database session.
        
    Raises:
        HTTPException 404: If the application is not found.
        
    Returns:
        Application: The application object.
    """
    result = await db.execute(select(Application).filter(Application.id == int(application_id)))
    app = result.scalars().first()
    if not app:
        raise HTTPException(404, "Application not found")
    return app

async def update_application_status(application_id: str, body: ApplicationStatusUpdate, user_id: str, db: AsyncSession):
    """
    Update the status of a rental application (Approve/Reject).
    Approving an application will automatically reject all other pending applications for the same property.
    
    Args:
        application_id (str): The application ID.
        body (ApplicationStatusUpdate): The status update details.
        user_id (str): The user ID of the seller/admin updating the status.
        db (AsyncSession): The database session.
        
    Raises:
        HTTPException 400: If the status is invalid or the application is not PENDING.
        HTTPException 404: If the application is not found.
        HTTPException 403: If the user does not own the property.
        
    Returns:
        dict: A success message.
    """
    if body.status not in ("APPROVED", "REJECTED"):
        raise HTTPException(400, "Status must be APPROVED or REJECTED")
    if body.status == "REJECTED" and not body.reason:
        raise HTTPException(400, "Reason required when rejecting")

    result = await db.execute(select(Application).filter(Application.id == int(application_id)))
    app = result.scalars().first()
    if not app:
        raise HTTPException(404, "Application not found")
    if app.status != "PENDING":
        raise HTTPException(400, "Only PENDING applications can be reviewed")

    result = await db.execute(select(Property).filter(Property.id == app.property_id))
    prop = result.scalars().first()
    if not prop or prop.owner_id != int(user_id):
        raise HTTPException(403, "You do not own this property")

    try:
        if body.status == "APPROVED":
            app.status = "APPROVED"
            
            # Reject others
            result = await db.execute(select(Application).filter(
                Application.property_id == app.property_id,
                Application.status == 'PENDING',
                Application.id != int(application_id)
            ))
            other_apps = result.scalars().all()
            for other in other_apps:
                other.status = "REJECTED"
                other.reason = "Another applicant was selected"
            
            # Auto-create Lease
            from app.schemas.lease_schema import LeaseCreate
            from app.services.lease_service import create_lease
            lease_body = LeaseCreate(application_id=str(application_id))
            await create_lease(lease_body, user_id, ["SELLER"], db)
            return {"message": "Application approved and lease generated."}
        else:
            app.status = "REJECTED"
            app.reason = body.reason
            await db.commit()
            return {"message": "Application rejected", "reason": body.reason}
    except Exception:
        await db.rollback()
        raise

async def delete_application(application_id: str, user_id: str, db: AsyncSession):
    """
    Delete a pending rental application.
    
    Args:
        application_id (str): The application ID.
        user_id (str): The user ID of the applicant.
        db (AsyncSession): The database session.
        
    Raises:
        HTTPException 404: If the application is not found.
        HTTPException 403: If the user does not own the application.
        HTTPException 400: If the application is not PENDING.
        
    Returns:
        dict: A success message.
    """
    result = await db.execute(select(Application).filter(Application.id == int(application_id)))
    app = result.scalars().first()
    if not app:
        raise HTTPException(404, "Application not found")
    if app.applicant_id != int(user_id):
        raise HTTPException(403, "You can only delete your own applications")
    if app.status != "PENDING":
        raise HTTPException(400, "Only PENDING applications can be deleted")
    
    try:
        await db.delete(app)
        await db.commit()
    except Exception:
        await db.rollback()
        raise
    return {"message": "Application deleted successfully"}

async def save_application_document(application_id: str, url: str, db: AsyncSession):
    """
    Save the uploaded government ID document URL to the application.
    
    Args:
        application_id (str): The application ID.
        url (str): The uploaded document URL.
        db (AsyncSession): The database session.
        
    Raises:
        HTTPException 404: If the application is not found.
        
    Returns:
        dict: A success message and the URL.
    """
    result = await db.execute(select(Application).filter(Application.id == int(application_id)))
    app = result.scalars().first()
    if not app:
        raise HTTPException(404, "Application not found")
    app.gov_id_url = url
    try:
        await db.commit()
    except Exception:
        await db.rollback()
        raise
    return {"message": "Document saved successfully", "url": url}
