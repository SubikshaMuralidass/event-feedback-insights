from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class FeedbackCreate(BaseModel):
    event_id: int
    attendee_name: str = Field(min_length=2, max_length=100)
    comment: str = Field(min_length=5)

class FeedbackResponse(FeedbackCreate):
    id: int
    created_at: datetime

    class Config:
        #orm_mode = True
        from_attributes = True
        
class FeedbackUpdate(BaseModel):
    attendee_name: Optional[str] = Field(None, min_length=2, max_length=100)
    comment: Optional[str] = Field(None, min_length=5)
