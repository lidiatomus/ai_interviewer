from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base


class Interview(Base):
    __tablename__ = "interviews"

    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String, nullable=False)
    status = Column(String, default="in_progress")

    summary = Column(Text, nullable=True)
    sentiment = Column(String, nullable=True)
    keywords = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    # relationships
    questions = relationship("Question", back_populates="interview", cascade="all, delete")
    answers = relationship("Answer", back_populates="interview", cascade="all, delete")


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    interview_id = Column(Integer, ForeignKey("interviews.id"))
    question_order = Column(Integer)
    question_text = Column(Text, nullable=False)

    # relationships
    interview = relationship("Interview", back_populates="questions")
    answer = relationship("Answer", back_populates="question", uselist=False)


class Answer(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, index=True)
    interview_id = Column(Integer, ForeignKey("interviews.id"))
    question_id = Column(Integer, ForeignKey("questions.id"))

    answer_text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # relationships
    interview = relationship("Interview", back_populates="answers")
    question = relationship("Question", back_populates="answer")