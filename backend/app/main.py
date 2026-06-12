"""Main FastAPI application entrypoint.

The test suite expects `from app.main import app`.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.db.database import init_db
from app.api.routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    init_db()
    yield
    # Shutdown


app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "application": settings.API_TITLE,
        "version": settings.API_VERSION,
    }


@app.get("/")
async def root():
    return {
        "message": "ResumeBoost AI API",
        "version": settings.API_VERSION,
        "docs": "/docs",
    }

