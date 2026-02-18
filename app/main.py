import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from contextlib import asynccontextmanager

from .db import Base, engine as default_engine
from .routes import router

# Detect if we are in testing mode
TESTING = os.getenv("TESTING") == "1"

# Use a different engine for tests
if TESTING:
    from sqlalchemy import create_engine
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
else:
    engine = default_engine
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up…")
    # Create tables if they don’t exist
    Base.metadata.create_all(bind=engine)
    yield
    print("Shutting down…")

# Initialize app with lifespan
app = FastAPI(lifespan=lifespan)

# Include API routes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)
