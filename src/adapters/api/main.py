"""Factory de la aplikación FastAPI con todos los routers registrados."""
import warnings

from fastapi import FastAPI

from src.adapters.api.routes.assessment_routes import router as assessment_router
from src.adapters.api.routes.auth_routes import router as auth_router
from src.adapters.api.routes.instructor_routes import router as instructor_router
from src.adapters.api.routes.message_routes import router as message_router
from src.adapters.api.routes.nutrition_routes import router as nutrition_router
from src.adapters.api.routes.physical_routes import router as physical_router
from src.adapters.api.routes.training_routes import router as training_router

from src.adapters.api.routes.user_routes import router as user_router
from src.infrastructure.database.base import Base
from src.infrastructure.database.session import engine

# Supress datetime.utcnow deprecation from SQLAlchemy internals
warnings.filterwarnings("ignore", category=DeprecationWarning)


def create_app() -> FastAPI:
    app = FastAPI(
        title="FitLife API",
        version="1.0.0",
        description="Backend FitLife - Arquitectura Hexagonal",
        docs_url="/docs",
        redoc_url="/redoc",
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

    # Auth & Users
    app.include_router(auth_router)
    app.include_router(user_router)

    # Domain features
    app.include_router(assessment_router)
    app.include_router(physical_router)
    app.include_router(instructor_router)

    app.include_router(training_router)
    app.include_router(nutrition_router)
    app.include_router(message_router)
