from contextlib import asynccontextmanager

from fastapi import FastAPI

from cairn.database import Base, engine
from cairn.routers import entries, hikes, games, media, workouts, mood
import cairn.models  # noqa: F401 - ensures all models are registered


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on startup
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Cairn",
    description="Self-hosted personal data logger",
    lifespan=lifespan,
)

app.include_router(entries.router)
app.include_router(hikes.router)
app.include_router(games.router)
app.include_router(media.router)
app.include_router(workouts.router)
app.include_router(mood.router)


@app.get("/health")
def health():
    return {"status": "ok"}
