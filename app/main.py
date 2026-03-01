from dotenv import load_dotenv
load_dotenv()

from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.config import *
from app.db.session import DBSession
from app.api.auth import router as auth_router
from app.api.tasks import router as tasks_router
from app.api.habits import router as habits_router
import app.models.user

@asynccontextmanager
async def lifespan(app: FastAPI):
    db = DBSession()
    try:
        print('Database Connection Successful')
    finally:
        db.close()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(auth_router)
app.include_router(tasks_router)
app.include_router(habits_router)

name = APP_NAME
version = APP_VERSION
environment = ENVIRONMENT

@app.get("/")
def read_root():
    return {
        'name': 'Personal Productivity API',
        'version': version,
        'environment': environment,
        'docs': '/docs',
        'redoc': '/redoc'
    }

@app.get('/health')
def health_check():
    return {
    'status': 'ok',
    'name': name,
    'version': version,
    'environment': environment}