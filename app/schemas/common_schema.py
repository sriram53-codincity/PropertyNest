from pydantic import BaseModel
from typing import Optional, Literal

class ApplicationStatusUpdate(BaseModel):
    status: Literal["APPROVED", "REJECTED"]
    reason: Optional[str] = None

class AppointmentStatusUpdate(BaseModel):
    status: Literal["CONFIRMED", "REJECTED", "COMPLETED", "CANCELLED"]
    reason: Optional[str] = None

class SellerRequestStatusUpdate(BaseModel):
    status: Literal["APPROVED", "REJECTED"]
    reason: Optional[str] = None

class PropertyStatusUpdate(BaseModel):
    status: Literal["PUBLISHED", "REJECTED", "ARCHIVED"]
    reason: Optional[str] = None
