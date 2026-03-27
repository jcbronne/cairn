from fastapi import FastAPI
from cairn.routers import entries, hikes, games, media, workouts, mood

app = FastAPI(title="Cairn", description="Self-hosted personal data logger")

app.include_router(entries.router)
app.include_router(hikes.router)
app.include_router(games.router)
app.include_router(media.router)
app.include_router(workouts.router)
app.include_router(mood.router)


@app.get("/health")
def health():
    return {"status": "ok"}
