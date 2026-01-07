from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from .database import Base

class EventFeedback(Base):
    __tablename__ = "event_feedback"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, index=True) # Foreign key to the event
    attendee_name = Column(String(100), nullable=False)
    comment = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
class EventSummary(Base):
    __tablename__ = "event_summaries"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, index=True, unique=True)
    summary = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
