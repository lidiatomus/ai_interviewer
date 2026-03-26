from pydantic import BaseModel


class StartInterviewRequest(BaseModel):
    topic: str


class AnswerRequest(BaseModel):
    question_index: int
    answer_text: str