from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.interview import StartInterviewRequest, AnswerRequest
from app.services.interview_service import (
    create_interview,
    save_answer,
    finish_interview,
    get_interview_details,
)

router = APIRouter(prefix="/interviews", tags=["interviews"])


@router.post("/start")
def start_interview(payload: StartInterviewRequest, db: Session = Depends(get_db)):
    try:
        return create_interview(db, payload.topic)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{interview_id}/answer")
def submit_answer(
    interview_id: int,
    payload: AnswerRequest,
    db: Session = Depends(get_db)
):
    try:
        return save_answer(db, interview_id, payload.question_index, payload.answer_text)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{interview_id}/finish")
def complete_interview(interview_id: int, db: Session = Depends(get_db)):
    try:
        return finish_interview(db, interview_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{interview_id}")
def get_interview(interview_id: int, db: Session = Depends(get_db)):
    try:
        return get_interview_details(db, interview_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))