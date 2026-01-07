from sqlalchemy.orm import Session
from .models import EventFeedback, EventSummary
from .schemas import FeedbackUpdate


def create_feedback(db: Session, feedback):
    db_feedback = EventFeedback(
        event_id=feedback.event_id,
        attendee_name=feedback.attendee_name,
        comment=feedback.comment
    )
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback

def get_feedback_by_id(db: Session, feedback_id: int):
    return db.query(EventFeedback).filter(EventFeedback.id == feedback_id).first()

def update_feedback(db: Session, feedback_id: int, feedback_data: FeedbackUpdate):
    feedback = db.query(EventFeedback).filter(EventFeedback.id == feedback_id).first()

    if not feedback:
        return None

    if feedback_data.attendee_name is not None:
        feedback.attendee_name = feedback_data.attendee_name

    if feedback_data.comment is not None:
        feedback.comment = feedback_data.comment

    db.commit()
    db.refresh(feedback)
    return feedback

def delete_feedback(db: Session, feedback_id: int) -> bool:
    feedback = db.query(EventFeedback).filter(EventFeedback.id == feedback_id).first()

    if not feedback:
        return False

    db.delete(feedback)
    db.commit()
    return True

def get_feedback_comments(db: Session, event_id: int):
    return [
        f.comment
        for f in db.query(EventFeedback)
        .filter(EventFeedback.event_id == event_id)
        .all()
    ]

def save_event_summary(db: Session, summary: str):
    event_summary = EventSummary(summary=summary)
    db.add(event_summary)
    db.commit()
    db.refresh(event_summary)
    return event_summary

