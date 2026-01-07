from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from .database import SessionLocal
from .schemas import FeedbackCreate, FeedbackResponse, FeedbackUpdate
from .crud import create_feedback, get_feedback_by_id, update_feedback, delete_feedback, get_feedback_comments, save_event_summary
from app.services.llm import summarize_feedback


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/feedback", response_model=FeedbackResponse, status_code=201)
def add_feedback(feedback: FeedbackCreate, db: Session = Depends(get_db)):
    return create_feedback(db, feedback)

@router.get("/feedback/{feedback_id}", response_model=FeedbackResponse)
def get_feedback(feedback_id: int, db: Session = Depends(get_db)):
    feedback = get_feedback_by_id(db, feedback_id)
    
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    
    return feedback

@router.put("/feedback/{feedback_id}", response_model=FeedbackResponse)
def update_feedback_endpoint(
    feedback_id: int,
    feedback_data: FeedbackUpdate,
    db: Session = Depends(get_db)
):
    updated_feedback = update_feedback(db, feedback_id, feedback_data)

    if not updated_feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")

    return updated_feedback

@router.delete("/feedback/{feedback_id}", status_code=204)
def delete_feedback_endpoint(
    feedback_id: int,
    db: Session = Depends(get_db)
):
    success = delete_feedback(db, feedback_id)

    if not success:
        raise HTTPException(status_code=404, detail="Feedback not found")

    return Response(status_code=204)


@router.post("/events/{event_id}/summary")
def generate_event_summary(
    event_id: int,
    db: Session = Depends(get_db)
):
    comments = get_feedback_comments(db, event_id)

    if not comments:
        raise HTTPException(status_code=404, detail="No feedback found for event")

    summary_text = summarize_feedback(comments)

    saved_summary = save_event_summary(db, event_id, summary_text)

    return {
        "event_id": event_id,
        "summary": saved_summary.summary
    }
