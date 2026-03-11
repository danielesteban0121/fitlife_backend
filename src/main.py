from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.adapters.api.middleware.error_handler import domain_exception_handler
from src.adapters.api.routes.assessment_routes import router as assessment_router
from src.adapters.api.routes.auth_routes import router as auth_router
from src.domain.exceptions.base import DomainException
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from src.config.limiter import limiter


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

    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    from fastapi.middleware.cors import CORSMiddleware

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # En produccion usar settings.CORS_ORIGINS
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/healthz", tags=["Health"])
    async def health_check():
        return {"status": "ok"}

    # Routers
    app.include_router(auth_router)
    app.include_router(assessment_router)

    from src.adapters.api.routes.instructor_routes import router as instructor_router
    from src.adapters.api.routes.training_routes import router as training_router
    from src.adapters.api.routes.nutrition_routes import router as nutrition_router
    from src.adapters.api.routes.message_routes import router as message_router

    app.include_router(instructor_router)
    app.include_router(training_router)
    app.include_router(nutrition_router)
    app.include_router(message_router)

    # Exception handlers
    app.add_exception_handler(
        DomainException,
        domain_exception_handler,
    )

    return app


app = create_app()
