import uvicorn
from fastapi import FastAPI
from db import engine, SessionLocal, Base