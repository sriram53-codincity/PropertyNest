from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.database.connection import get_db
from app.auth import get_current_user, require_roles
from app.schemas.application_schema import ApplicationCreate
from app.schemas.common_schema import StatusUpdate
from app.services import application_service

router = APIRouter(prefix="/api/applications", tags=["Applications"])

@router.post("/")
def apply(
    body: ApplicationCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """BUYER: Submit a rental application using JSON."""
    return application_service.submit_application(body, current_user["user_id"], db)


@router.get("/")
def list_applications(
    property_id: Optional[str] = Query(None),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return application_service.list_applications(
        property_id, current_user["user_id"], current_user.get("roles", []), db
    )


@router.get("/{application_id}")
def get_application(application_id: str, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    return application_service.get_application(application_id, db)


@router.patch("/{application_id}/status")
def update_application_status(
    application_id: str,
    body: StatusUpdate,
    current_user: dict = Depends(require_roles("SELLER", "ADMIN")),
    db: Session = Depends(get_db)
):
    return application_service.update_application_status(application_id, body, db)

@router.delete("/{application_id}")
def delete_application(
    application_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """BUYER: Withdraw/delete your pending application."""
    return application_service.delete_application(application_id, current_user["user_id"], db)
