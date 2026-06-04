from pydantic import BaseModel
from typing import Optional, Literal

class StatusUpdate(BaseModel):
    status: Literal["PENDING", "APPROVED", "REJECTED", "PUBLISHED", "CONFIRMED"]
    reason: Optional[str] = None
