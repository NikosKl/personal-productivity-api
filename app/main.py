from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.config import *
from app.db.session import DBSession
from app.db.session import engine
from app.db.base import Base
import app.models.user

@asynccontextmanager
async def lifespan(app: FastAPI):
    db = DBSession()
    try:
        print('Database Connection Successful')
        Base.metadata.create_all(bind=engine)
    finally:
        db.close()
    yield
app = FastAPI(lifespan=lifespan)

name = APP_NAME
version = APP_VERSION
environment = ENVIRONMENT
@app.get("/")
def read_root():
    pass

@app.get('/health')
def health_check():
    return {
    'status': 'ok',
    'name': name,
    'version': version,
    'environment': environment}