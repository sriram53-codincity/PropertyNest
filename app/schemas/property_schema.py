from pydantic import BaseModel
from typing import Optional, Literal, List
from decimal import Decimal

class PropertyCreate(BaseModel):
    title:         str
    city:          str
    property_type: Literal["APARTMENT", "HOUSE", "VILLA", "STUDIO", "COMMERCIAL"]
    bedrooms:      int = 1
    bathrooms:     int = 1
    monthly_rent:  Decimal
    description:   Optional[str] = ""
    amenities:     Optional[List[str]] = []

class PropertyUpdate(BaseModel):
    """All fields are optional — only send what you want to change."""
    title:         Optional[str]   = None
    city:          Optional[str]   = None
    property_type: Optional[str]   = None
    bedrooms:      Optional[int]   = None
    bathrooms:     Optional[int]   = None
    monthly_rent:  Optional[Decimal] = None
    is_available:  Optional[bool]  = None
    status:        Optional[Literal["PENDING", "PUBLISHED", "REJECTED", "ARCHIVED"]] = None
    reason:        Optional[str]   = None
    description:   Optional[str]   = None
    amenities:     Optional[List[str]]  = None
