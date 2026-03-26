import json
import os
from app.db.models import Interview, Question, Answer
from sqlalchemy.orm import Session


EXPORT_DIR = "app/exports"


def export_interview_to_json(db: Session, interview_id: int) -> str:
    interview = db.query(Interview).filter(Interview.id == interview_id).first()
    if not interview:
        raise ValueError("Interview not found")

    questions = (
        db.query(Question)
        .filter(Question.interview_id == interview_id)
        .order_by(Question.question_order)
        .all()
    )

    transcript = []
    for question in questions:
        answer = (
            db.query(Answer)
            .filter(
                Answer.interview_id == interview_id,
                Answer.question_id == question.id
            )
            .first()
        )

        transcript.append({
            "question_index": question.question_order,
            "question_text": question.question_text,
            "answer_text": answer.answer_text if answer else None
        })

    data = {
        "interview_id": interview.id,
        "topic": interview.topic,
        "status": interview.status,
        "summary": interview.summary,
        "sentiment": interview.sentiment,
        "keywords": json.loads(interview.keywords) if interview.keywords else [],
        "transcript": transcript
    }

    os.makedirs(EXPORT_DIR, exist_ok=True)
    file_path = os.path.join(EXPORT_DIR, f"interview_{interview.id}.json")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    return file_path