from fastapi import FastAPI
from app.core.config import *

app = FastAPI()

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