from pydantic import BaseModel
from typing import Optional, Literal

class ApplicationCreate(BaseModel):
    property_id:     str
    full_name:       str
    email:           str
    phone:           str
    date_of_birth:   str               # YYYY-MM-DD
    marital_status:  Literal["SINGLE", "MARRIED", "DIVORCED", "WIDOWED"]
    employment_type: Literal["STUDENT", "EMPLOYED", "SELF_EMPLOYED", "UNEMPLOYED"]
    college_name:    Optional[str]     = None
    company_name:    Optional[str]     = None
    monthly_income:  Optional[float]   = None
    current_address: str
    move_in_date:    str               # YYYY-MM-DD
    lease_duration:  int               # months
    num_occupants:   int               = 1
    additional_notes: Optional[str]    = None
