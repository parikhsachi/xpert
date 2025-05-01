from fastapi import FastAPI
from app.api import ask

app = FastAPI(title="Xpert.ai API")

app.include_router(ask.router, prefix="/api/v1")