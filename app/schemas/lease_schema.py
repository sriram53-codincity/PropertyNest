from pydantic import BaseModel

class LeaseCreate(BaseModel):
    application_id: str
