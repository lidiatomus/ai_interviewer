from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import DATABASE_URL

# create engine
engine = create_engine(DATABASE_URL)

# create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# base class for models
Base = declarative_base()


# dependency (used later in routes)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()