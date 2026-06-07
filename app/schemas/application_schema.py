from pydantic import BaseModel, EmailStr
from typing import Optional, Literal
from datetime import date
from decimal import Decimal

class ApplicationCreate(BaseModel):
    property_id:     str
    full_name:       str
    email:           EmailStr
    phone:           str
    date_of_birth:   date
    marital_status:  Literal["SINGLE", "MARRIED", "DIVORCED", "WIDOWED"]
    employment_type: Literal["STUDENT", "EMPLOYED", "SELF_EMPLOYED", "UNEMPLOYED"]
    college_name:    Optional[str]     = None
    company_name:    Optional[str]     = None
    monthly_income:  Optional[Decimal]   = None
    current_address: str
    move_in_date:    date
    lease_duration:  int               # months
    num_occupants:   int               = 1
    additional_notes: Optional[str]    = None
