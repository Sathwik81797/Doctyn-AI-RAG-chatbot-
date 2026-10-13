from pydantic import BaseModel
from typing import Optional


class ChatRequestV2(BaseModel):
    message: str
    session_id: Optional[str] = None
    page_context: Optional[str] = None


class LeadRequestV2(BaseModel):
    name: Optional[str] = None
    qualification: Optional[str] = None
    city: Optional[str] = None
    experience: Optional[str] = None
    interest: Optional[str] = None
    employment_status: Optional[str] = None
    learning_preference: Optional[str] = None
    clinical_training_available: Optional[str] = None
    message: Optional[str] = None
