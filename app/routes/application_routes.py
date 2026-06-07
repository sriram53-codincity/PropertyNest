import os
import uuid
from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.connection import get_db
from app.auth import get_current_user, require_roles
from app.schemas.application_schema import ApplicationCreate, ApplicationResponse
from app.schemas.common_schema import ApplicationStatusUpdate
from app.services import application_service

router = APIRouter(prefix="/api/applications", tags=["Applications"])
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")

# @router.post("/", response_model=ApplicationResponse)
@router.post("/", response_model=ApplicationResponse, dependencies=[Depends(require_roles("TENANT", "BUYER", "ADMIN"))])
async def create_application(
    body: ApplicationCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return await application_service.create_application(body, current_user["user_id"], db)

@router.get("/", dependencies=[Depends(require_roles("SELLER", "ADMIN"))])
async def get_applications(db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return await application_service.get_applications(current_user["user_id"], current_user.get("roles", []), db)

@router.get("/{application_id}")
async def get_application(application_id: str, db: AsyncSession = Depends(get_db)):
    return await application_service.get_application(application_id, db)

@router.patch("/{application_id}/status")
async def update_application_status(
    application_id: str,
    body: ApplicationStatusUpdate,
    current_user: dict = Depends(require_roles("SELLER")),
    db: AsyncSession = Depends(get_db)
):
    return await application_service.update_application_status(application_id, body, current_user["user_id"], db)

@router.delete("/{application_id}")
async def delete_application(
    application_id: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await application_service.delete_application(application_id, current_user["user_id"], db)

@router.post("/{application_id}/document")
async def upload_document(
    application_id: str,
    document: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """BUYER: Upload a payslip or ID document for the application."""
    folder = os.path.join(UPLOAD_DIR, "application_documents", application_id)
    os.makedirs(folder, exist_ok=True)

    data = await document.read()
    safe_filename = f"{uuid.uuid4()}_{os.path.basename(document.filename)}"
    file_path = os.path.join(folder, safe_filename)
    with open(file_path, "wb") as f:
        f.write(data)
    
    url = f"/uploads/application_documents/{application_id}/{safe_filename}"
    return await application_service.save_application_document(application_id, url, db)
