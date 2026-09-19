from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers import entities, graph
from app.core.config import settings

app = FastAPI(title=settings.app_name, version=settings.app_version)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.frontend_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(entities.router)
app.include_router(graph.router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
