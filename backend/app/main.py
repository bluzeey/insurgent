from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.persistence.in_memory import InMemoryStore


def create_app() -> FastAPI:
    app = FastAPI(
        title="Insurance Information Agent API",
        version="0.1.0",
        description="M1 dry-run API: instruction to approved plan to synthetic result. No real outbound actions.",
    )
    app.state.store = InMemoryStore()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(router)
    return app


app = create_app()
