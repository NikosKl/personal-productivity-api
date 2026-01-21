from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.config import *
from app.db.session import Session

@asynccontextmanager
async def lifespan(app: FastAPI):
    db = Session()
    try:
        print('Database Connection Successful')
    finally:
        db.close()
    yield
app = FastAPI(lifespan=lifespan)

name = APP_NAME
version = APP_VERSION
environment = ENVIRONMENT
@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get('/health')
def health_check():
    return {
    'status': 'ok',
    'name': name,
    'version': version,
    'environment': environment}