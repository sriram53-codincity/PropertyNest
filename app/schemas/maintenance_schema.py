from pydantic import BaseModel
from typing import Literal

class MaintenanceCreate(BaseModel):
    lease_id:    str
    title:       str
    category:    Literal["PLUMBING", "ELECTRICAL", "APPLIANCE", "CLEANING", "OTHER"]
    priority:    Literal["LOW", "MEDIUM", "HIGH"] = "LOW"
    description: str

class MaintenanceStatusUpdate(BaseModel):
    status:  Literal["OPEN", "IN_PROGRESS", "RESOLVED", "CLOSED"]
    comment: str   # Required — what was done
