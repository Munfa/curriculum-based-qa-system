"""FastAPI application factory."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routers import health, metadata, study


def create_app() -> FastAPI:
    application = FastAPI(title="Curriculum-Based Bangla QA System", version="1.0.0")
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    application.include_router(health.router)
    application.include_router(metadata.router)
    application.include_router(study.router)
    return application


app = create_app()
