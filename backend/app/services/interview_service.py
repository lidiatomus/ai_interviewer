import json
from datetime import datetime
from sqlalchemy.orm import Session

from app.db.models import Interview, Question, Answer
from app.services.openai_service import generate_questions, generate_summary
from app.services.export_service import export_interview_to_json

def create_interview(db: Session, topic: str) -> dict:
    interview = Interview(topic=topic, status="in_progress")
    db.add(interview)
    db.commit()
    db.refresh(interview)

    questions = generate_questions(topic)

    saved_questions = []
    for index, question_text in enumerate(questions):
        question = Question(
            interview_id=interview.id,
            question_order=index,
            question_text=question_text
        )
        db.add(question)
        saved_questions.append(question)

    db.commit()

    first_question = saved_questions[0].question_text if saved_questions else None

    return {
        "interview_id": interview.id,
        "question_index": 0,
        "question_text": first_question
    }


def save_answer(db: Session, interview_id: int, question_index: int, answer_text: str) -> dict:
    interview = db.query(Interview).filter(Interview.id == interview_id).first()
    if not interview:
        raise ValueError("Interview not found")

    question = (
        db.query(Question)
        .filter(
            Question.interview_id == interview_id,
            Question.question_order == question_index
        )
        .first()
    )

    if not question:
        raise ValueError("Question not found")

    existing_answer = (
        db.query(Answer)
        .filter(
            Answer.interview_id == interview_id,
            Answer.question_id == question.id
        )
        .first()
    )

    if existing_answer:
        existing_answer.answer_text = answer_text
    else:
        new_answer = Answer(
            interview_id=interview_id,
            question_id=question.id,
            answer_text=answer_text
        )
        db.add(new_answer)

    db.commit()

    next_question = (
        db.query(Question)
        .filter(
            Question.interview_id == interview_id,
            Question.question_order == question_index + 1
        )
        .first()
    )

    if next_question:
        return {
            "done": False,
            "next_question_index": next_question.question_order,
            "next_question_text": next_question.question_text
        }

    return {"done": True}


def finish_interview(db: Session, interview_id: int) -> dict:
    interview = db.query(Interview).filter(Interview.id == interview_id).first()
    if not interview:
        raise ValueError("Interview not found")

    questions = (
        db.query(Question)
        .filter(Question.interview_id == interview_id)
        .order_by(Question.question_order)
        .all()
    )

    qa_pairs = []
    for question in questions:
        answer = (
            db.query(Answer)
            .filter(
                Answer.interview_id == interview_id,
                Answer.question_id == question.id
            )
            .first()
        )

        qa_pairs.append({
            "question": question.question_text,
            "answer": answer.answer_text if answer else ""
        })

    result = generate_summary(interview.topic, qa_pairs)

    interview.summary = result.get("summary")
    interview.sentiment = result.get("sentiment")
    interview.keywords = json.dumps(result.get("keywords", []))
    interview.status = "completed"
    interview.completed_at = datetime.utcnow()

    db.commit()
    export_path = export_interview_to_json(db, interview_id)

    return {
        "summary": interview.summary,
        "sentiment": interview.sentiment,
        "keywords": result.get("keywords", []),
        "export_path": export_path
    }


def get_interview_details(db: Session, interview_id: int) -> dict:
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

    return {
        "interview_id": interview.id,
        "topic": interview.topic,
        "status": interview.status,
        "summary": interview.summary,
        "sentiment": interview.sentiment,
        "keywords": json.loads(interview.keywords) if interview.keywords else [],
        "transcript": transcript
    }