from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.adapters.api.middleware.error_handler import domain_exception_handler
from src.adapters.api.routes.assessment_routes import router as assessment_router
from src.adapters.api.routes.auth_routes import router as auth_router
from src.domain.exceptions.base import DomainException


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Application startup")
    yield
    print("🛑 Application shutdown")


def create_app() -> FastAPI:
    app = FastAPI(
        title="FitLife API",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )

    @app.get("/healthz", tags=["Health"])
    async def health_check():
        return {"status": "ok"}

    # Routers
    app.include_router(auth_router)
    app.include_router(assessment_router)

    # Exception handlers
    app.add_exception_handler(
        DomainException,
        domain_exception_handler,
    )

    return app


app = create_app()
