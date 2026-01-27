from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import DATABASE_URL

engine = create_engine(DATABASE_URL)

DBSession = sessionmaker(bind=engine)

def get_db():
    db = DBSession()
    try:
        yield db
    finally:
        db.close()