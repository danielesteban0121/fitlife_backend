from fastapi import FastAPI


def create_app() -> FastAPI:
    app = FastAPI(
        title="FitLife API",
        version="1.0.0",
        description="Backend FitLife - Arquitectura Hexagonal",
    )

    register_routes(app)

    return app


def register_routes(app: FastAPI) -> None:
    @app.get("/healthz", tags=["Health"])
    async def health_check():
        return {"status": "ok"}
