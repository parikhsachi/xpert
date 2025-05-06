from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import ask
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(title="Xpert.ai API")

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["POST"],
  allow_headers=["*"],
)

app.include_router(ask.router, prefix="/api/v1")