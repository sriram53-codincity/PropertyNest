import os
import uuid
from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, Literal
from app.database.connection import get_db
from app.auth import get_current_user, require_roles
from app.schemas.common_schema import SellerRequestStatusUpdate
from app.services import seller_request_service

router = APIRouter(prefix="/api/seller-requests", tags=["Seller Requests"])

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")


@router.post("/")
async def create_seller_request(
    full_name:        str         = Form(...),
    phone:            str         = Form(...),
    address:          str         = Form(...),
    property_title:   str         = Form(...),
    property_address: str         = Form(...),
    district:         str         = Form(...),
    property_type:    str         = Form(...),
    bedrooms:         int         = Form(...),
    monthly_rent:     float       = Form(...),
    description:      str         = Form(""),
    doc_type:         str         = Form(...),
    declaration_accepted: bool    = Form(...),
    ownership_doc:    UploadFile   = File(...),
    property_image:   UploadFile  = File(...),
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    user_id = current_user["user_id"]

    folder = os.path.join(UPLOAD_DIR, "ownership_docs")
    os.makedirs(folder, exist_ok=True)
    doc_bytes = await ownership_doc.read()
    safe_doc_name = f"{uuid.uuid4()}_{os.path.basename(ownership_doc.filename)}"
    with open(os.path.join(folder, safe_doc_name), "wb") as f:
        f.write(doc_bytes)
    doc_url = f"/uploads/ownership_docs/{safe_doc_name}"

    img_folder = os.path.join(UPLOAD_DIR, "property_images")
    os.makedirs(img_folder, exist_ok=True)
    
    img_data = await property_image.read()
    safe_img_name = f"{uuid.uuid4()}_{os.path.basename(property_image.filename)}"
    with open(os.path.join(img_folder, safe_img_name), "wb") as f:
        f.write(img_data)
    image_url = f"/uploads/property_images/{safe_img_name}"

    return await seller_request_service.create_seller_request(
        user_id, full_name, phone, address, property_title, property_address, district,
        property_type, bedrooms, monthly_rent, description, doc_type, declaration_accepted, doc_url, [image_url], db
    )


@router.get("/mine")
async def my_requests(current_user: dict = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await seller_request_service.get_my_requests(current_user["user_id"], db)


@router.get("/")
async def all_requests(
    status: Optional[Literal["PENDING", "APPROVED", "REJECTED"]] = None,
    current_user: dict = Depends(require_roles("ADMIN")),
    db: AsyncSession = Depends(get_db)
):
    return await seller_request_service.get_all_requests(status, db)


@router.patch("/{request_id}/status")
async def update_status(
    request_id: str,
    body: SellerRequestStatusUpdate,
    current_user: dict = Depends(require_roles("ADMIN")),
    db: AsyncSession = Depends(get_db)
):
    return await seller_request_service.update_status(request_id, body, db)

@router.delete("/{request_id}")
async def delete_request(
    request_id: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """USER: Cancel/delete your pending seller request."""
    return await seller_request_service.delete_request(request_id, current_user["user_id"], db)
