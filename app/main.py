from dotenv import load_dotenv
load_dotenv()

from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.config import *
from app.db.session import DBSession
from app.api.auth import router as auth_router
from app.api.tasks import router as tasks_router
from app.api.habits import router as habits_router
from app.api.analytics import router as analytics_router
import app.models.user
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler
from app.core.rate_limit import limiter

@asynccontextmanager
async def lifespan(app: FastAPI):
    db = DBSession()
    try:
        print('Database Connection Successful')
    finally:
        db.close()
    yield

app = FastAPI(lifespan=lifespan)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

app.include_router(auth_router)
app.include_router(tasks_router)
app.include_router(habits_router)
app.include_router(analytics_router)

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