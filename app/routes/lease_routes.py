from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.auth import get_current_user, require_roles
from app.schemas.lease_schema import LeaseCreate
from app.services import lease_service

router = APIRouter(prefix="/api/leases", tags=["Leases"])

@router.post("/")
def create_lease(
    body: LeaseCreate,
    current_user: dict = Depends(require_roles("SELLER", "ADMIN")),
    db: Session = Depends(get_db)
):
    """SELLER: Create a lease for an APPROVED application."""
    return lease_service.create_lease(body, db)


@router.get("/me")
def my_leases(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    """View all your leases (as tenant or as property owner)."""
    return lease_service.get_my_leases(current_user["user_id"], db)


@router.get("/{lease_id}")
def get_lease(lease_id: str, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    """View a single lease detail with tenant and property info."""
    return lease_service.get_lease(
        lease_id, current_user["user_id"], current_user.get("roles", []), db
    )
