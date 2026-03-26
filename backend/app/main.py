from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import engine
from app.db.models import Base
from app.routes.interviews import router as interview_router

app = FastAPI(title="AI Interviewer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(interview_router)


@app.get("/")
def root():
    return {"message": "AI Interviewer backend is running"}