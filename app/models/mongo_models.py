from beanie import Document
from typing import List

class PropertyDetails(Document):
    property_id: str
    description: str = ""
    amenities: List[str] = []
    image_urls: List[str] = []
    inspection_reports: List[str] = []

    class Settings:
        name = "property_details"
