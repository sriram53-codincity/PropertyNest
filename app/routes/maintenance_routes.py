import os
import uuid
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.database.connection import get_db
from app.auth import get_current_user, require_roles
from app.schemas.maintenance_schema import MaintenanceCreate, MaintenanceStatusUpdate
from app.services import maintenance_service

router = APIRouter(prefix="/api/maintenance", tags=["Maintenance"])

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")

@router.post("/")
async def raise_request(
    body: MaintenanceCreate,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """TENANT: Raise a maintenance request via JSON."""
    return await maintenance_service.raise_request(body, current_user["user_id"], db)


@router.post("/{request_id}/images")
async def upload_maintenance_images(
    request_id: str,
    images: list[UploadFile] = File(...),
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    req = await maintenance_service.check_request_exists(request_id, db)
    if not req:
        raise HTTPException(404, "Maintenance request not found")

    image_urls = req.image_urls or []

    for img in images:
        folder = os.path.join(UPLOAD_DIR, "maintenance", str(req.lease_id))
        os.makedirs(folder, exist_ok=True)
        data = await img.read()
        safe_name = f"{uuid.uuid4()}_{os.path.basename(img.filename)}"
        with open(os.path.join(folder, safe_name), "wb") as f:
            f.write(data)
        image_urls.append(f"/uploads/maintenance/{req.lease_id}/{safe_name}")

    return await maintenance_service.upload_images(request_id, image_urls, db)


@router.get("/")
async def list_requests(
    property_id: Optional[str] = Query(None),
    lease_id:    Optional[str] = Query(None),
    status:      Optional[str] = Query(None),
    as_admin:    bool = Query(False),
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List maintenance requests. Filters: property_id, lease_id, status."""
    return await maintenance_service.list_requests(
        property_id, lease_id, status, as_admin, current_user["user_id"], current_user.get("roles", []), db
    )


@router.get("/{request_id}")
async def get_request(request_id: str, current_user: dict = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await maintenance_service.get_request(request_id, db)


@router.patch("/{request_id}/status")
async def update_status(
    request_id: str,
    body: MaintenanceStatusUpdate,
    current_user: dict = Depends(require_roles("SELLER", "ADMIN")),
    db: AsyncSession = Depends(get_db)
):
    """SELLER: Update the status of a maintenance request with a comment."""
    return await maintenance_service.update_status(request_id, body, db)

@router.delete("/{request_id}")
async def delete_request(
    request_id: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """TENANT: Cancel/delete your maintenance request."""
    return await maintenance_service.delete_request(request_id, current_user["user_id"], db)
