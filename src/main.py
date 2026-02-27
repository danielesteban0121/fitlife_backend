from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.adapters.api.routes.auth_routes import router as auth_router
from src.adapters.api.middleware.error_handler import domain_exception_handler
from src.domain.exceptions.base import DomainException


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 🔹 Código que antes estaba en @app.on_event("startup")
    print("🚀 Application startup")

    yield

    # 🔹 Código opcional de shutdown
    print("🛑 Application shutdown")


def create_app() -> FastAPI:
    app = FastAPI(
        title="FitLife API",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,  # 👈 aquí está la clave
    )

    # 🔹 Health check
    @app.get("/healthz", tags=["Health"])
    async def health_check():
        return {"status": "ok"}

    # 🔹 Routers
    app.include_router(auth_router)

    # 🔹 Exception handlers
    app.add_exception_handler(
        DomainException,
        domain_exception_handler,
    )

    return app


app = create_app()