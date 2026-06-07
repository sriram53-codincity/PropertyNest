import os
import uuid
from fastapi import APIRouter, Depends, UploadFile, File, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.database.connection import get_db
from app.auth import get_current_user, require_roles
from app.schemas.property_schema import PropertyCreate, PropertyUpdate
from app.services import property_service

router = APIRouter(prefix="/api/properties", tags=["Properties"])

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")

@router.get("/")
async def get_properties(
    city: Optional[str] = Query(None),
    property_type: Optional[str] = Query(None),
    min_rent: Optional[float] = Query(None),
    max_rent: Optional[float] = Query(None),
    available: Optional[bool] = Query(None),
    sort:          str             = Query("newest"),
    db: AsyncSession = Depends(get_db)
):
    """Public: List published properties with optional filters."""
    return await property_service.get_properties(db, city, property_type, min_rent, max_rent, available, sort)

@router.get("/admin/all")
async def get_all_properties_admin(
    current_user: dict = Depends(require_roles("ADMIN")),
    db: AsyncSession = Depends(get_db)
):
    """ADMIN: Get all properties including pending ones."""
    return await property_service.get_all_properties_admin(db)

@router.get("/mine")
async def get_my_properties(
    current_user: dict = Depends(require_roles("SELLER", "ADMIN")),
    db: AsyncSession = Depends(get_db)
):
    """SELLER: Get all properties owned by the current user."""
    return await property_service.get_my_properties(current_user["user_id"], db)


@router.get("/{property_id}")
async def get_property(property_id: str, db: AsyncSession = Depends(get_db)):
    """Get full property detail — PostgreSQL data merged with MongoDB description."""
    return await property_service.get_property(property_id, db)


@router.post("/")
async def create_property(
    body: PropertyCreate,
    current_user: dict = Depends(require_roles("SELLER", "ADMIN")),
    db: AsyncSession = Depends(get_db)
):
    """SELLER: Create a new property listing."""
    return await property_service.create_property(body, current_user["user_id"], db)


@router.patch("/{property_id}")
async def update_property(
    property_id: str,
    body: PropertyUpdate,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """SELLER: Update listing details. ADMIN: Can also update status."""
    return await property_service.update_property(
        property_id, body, current_user["user_id"], current_user.get("roles", []), db
    )


@router.post("/{property_id}/images")
async def upload_images(
    property_id: str,
    images: list[UploadFile] = File(...),
    current_user: dict = Depends(require_roles("SELLER", "ADMIN")),
):
    image_urls = []
    for img in images:
        folder = os.path.join(UPLOAD_DIR, "properties", property_id)
        os.makedirs(folder, exist_ok=True)
        data = await img.read()
        safe_name = f"{uuid.uuid4()}_{os.path.basename(img.filename)}"
        with open(os.path.join(folder, safe_name), "wb") as f:
            f.write(data)
        image_urls.append(f"/uploads/properties/{property_id}/{safe_name}")

    await property_service.save_property_images(property_id, image_urls)
    return {"message": f"{len(image_urls)} image(s) uploaded", "urls": image_urls}

@router.delete("/{property_id}")
async def delete_property(
    property_id: str,
    current_user: dict = Depends(require_roles("SELLER", "ADMIN")),
    db: AsyncSession = Depends(get_db)
):
    """SELLER: Delete your own property. ADMIN: Can delete any property."""
    return await property_service.delete_property(
        property_id, current_user["user_id"], current_user.get("roles", []), db
    )
