import os
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.database.connection import get_db
from app.auth import get_current_user, require_roles
from app.schemas.maintenance_schema import MaintenanceCreate, MaintenanceStatusUpdate
from app.services import maintenance_service

router = APIRouter(prefix="/api/maintenance", tags=["Maintenance"])

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")

@router.post("/")
def raise_request(
    body: MaintenanceCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """TENANT: Raise a maintenance request via JSON."""
    return maintenance_service.raise_request(body, current_user["user_id"], db)


@router.post("/{request_id}/images")
async def upload_maintenance_images(
    request_id: str,
    images: list[UploadFile] = File(...),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    req = maintenance_service.check_request_exists(request_id, db)
    if not req:
        raise HTTPException(404, "Maintenance request not found")

    image_urls = []
    if req.image_urls:
        image_urls = req.image_urls.split(",")

    for img in images:
        folder = os.path.join(UPLOAD_DIR, "maintenance", str(req.lease_id))
        os.makedirs(folder, exist_ok=True)
        data = await img.read()
        with open(os.path.join(folder, img.filename), "wb") as f:
            f.write(data)
        image_urls.append(f"/uploads/maintenance/{req.lease_id}/{img.filename}")

    return maintenance_service.upload_images(request_id, image_urls, db)


@router.get("/")
def list_requests(
    property_id: Optional[str] = Query(None),
    lease_id:    Optional[str] = Query(None),
    status:      Optional[str] = Query(None),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List maintenance requests. Filters: property_id, lease_id, status."""
    return maintenance_service.list_requests(
        property_id, lease_id, status, current_user["user_id"], current_user.get("roles", []), db
    )


@router.get("/{request_id}")
def get_request(request_id: str, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    return maintenance_service.get_request(request_id, db)


@router.patch("/{request_id}/status")
def update_status(
    request_id: str,
    body: MaintenanceStatusUpdate,
    current_user: dict = Depends(require_roles("SELLER", "ADMIN")),
    db: Session = Depends(get_db)
):
    """SELLER: Update the status of a maintenance request with a comment."""
    return maintenance_service.update_status(request_id, body, db)

@router.delete("/{request_id}")
def delete_request(
    request_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """TENANT: Cancel/delete your maintenance request."""
    return maintenance_service.delete_request(request_id, current_user["user_id"], db)
