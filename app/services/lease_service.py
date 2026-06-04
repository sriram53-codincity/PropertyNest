from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.orm import aliased
from dateutil.relativedelta import relativedelta
from app.models.pg_models import Lease, Application, Property, User
from app.schemas.lease_schema import LeaseCreate

def create_lease(body: LeaseCreate, db: Session):
    app = db.query(Application).filter(Application.id == body.application_id).first()
    
    if not app:
        raise HTTPException(404, "Application not found")
    if app.status != "APPROVED":
        raise HTTPException(400, "Application must be APPROVED to create a lease")

    existing_lease = db.query(Lease).filter(Lease.application_id == body.application_id).first()
    if existing_lease:
        raise HTTPException(400, "A lease already exists for this application")

    prop = db.query(Property).filter(Property.id == app.property_id).first()

    start_date = app.move_in_date
    end_date   = start_date + relativedelta(months=int(app.lease_duration))

    new_lease = Lease(
        property_id=app.property_id,
        tenant_id=app.applicant_id,
        owner_id=prop.owner_id,
        application_id=body.application_id,
        start_date=start_date,
        end_date=end_date,
        monthly_rent=prop.monthly_rent
    )
    db.add(new_lease)

    prop.is_available = False

    db.commit()
    db.refresh(new_lease)
    return {"message": "Lease created successfully", "lease": new_lease}


def get_my_leases(user_id: str, db: Session):
    Tenant = aliased(User)
    Owner = aliased(User)

    results = db.query(
        Lease,
        Property.title.label("property_title"),
        Property.city,
        Tenant.full_name.label("tenant_name"),
        Tenant.email.label("tenant_email"),
        Owner.full_name.label("owner_name")
    ).join(Property, Lease.property_id == Property.id)\
     .join(Tenant, Lease.tenant_id == Tenant.id)\
     .join(Owner, Lease.owner_id == Owner.id)\
     .filter((Lease.tenant_id == user_id) | (Lease.owner_id == user_id))\
     .order_by(Lease.created_at.desc())\
     .all()

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


def get_lease(lease_id: str, user_id: str, roles: list, db: Session):
    Tenant = aliased(User)
    Owner = aliased(User)

    result = db.query(
        Lease,
        Property.title.label("property_title"),
        Property.city,
        Tenant.full_name.label("tenant_name"),
        Tenant.email.label("tenant_email"),
        Owner.full_name.label("owner_name")
    ).join(Property, Lease.property_id == Property.id)\
     .join(Tenant, Lease.tenant_id == Tenant.id)\
     .join(Owner, Lease.owner_id == Owner.id)\
     .filter(Lease.id == lease_id)\
     .first()

    if not result:
        raise HTTPException(404, "Lease not found")

    lease, property_title, city, tenant_name, tenant_email, owner_name = result
    
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
