from fastapi import FastAPI

from src.adapters.api.routes.assessment_routes import router as assessment_router
from src.adapters.api.routes.auth_routes import router as auth_router
from src.infrastructure.database.base import Base
from src.infrastructure.database.session import engine


def create_app() -> FastAPI:
    app = FastAPI(
        title="FitLife API",
        version="1.0.0",
        description="Backend FitLife - Arquitectura Hexagonal",
    )

    @app.on_event("startup")
    async def startup():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    register_routes(app)

    return app


def register_routes(app: FastAPI):
    @app.get("/healthz", tags=["Health"])
    async def health_check():
        return {"status": "ok"}

    app.include_router(assessment_router)
    app.include_router(auth_router)
