from fastapi import APIRouter

router = APIRouter(prefix="/games", tags=["games"])

# TODO: implement following the hikes router pattern in routers/hikes.py
#
#   POST /games              — log a game session
#   GET  /games              — list (filter: tag, date, status, platform)
#   GET  /games/{id}         — single entry
#
# Models:  cairn/models/game.py     (Game, GameStatus)
# Schemas: cairn/schemas/game.py    (GameEntryCreate, GameEntryRead, GameDetails)
