from pydantic import BaseModel, EmailStr
from typing import Optional, Literal
from datetime import date

class AppointmentCreate(BaseModel):
    property_id:      Optional[int] = None
    full_name:        str
    email:            EmailStr
    phone:            str
    purpose:          Literal["PROPERTY_TOUR", "BECOME_SELLER", "LISTING_HELP", "RENTAL_SUPPORT", "MAINTENANCE_SUPPORT", "GENERAL_INQUIRY"]
    preferred_date:   date             # YYYY-MM-DD
    preferred_time:   str             # e.g. "10:00 AM"
    additional_notes: Optional[str] = None
