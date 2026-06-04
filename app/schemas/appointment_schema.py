from pydantic import BaseModel
from typing import Optional, Literal

class AppointmentCreate(BaseModel):
    full_name:        str
    email:            str
    phone:            str
    purpose:          Literal["PROPERTY_TOUR", "BECOME_SELLER", "LISTING_HELP", "RENTAL_SUPPORT", "MAINTENANCE_SUPPORT", "GENERAL_INQUIRY"]
    preferred_date:   str             # YYYY-MM-DD
    preferred_time:   str             # e.g. "10:00 AM"
    additional_notes: Optional[str] = None
