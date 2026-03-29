from fastapi import APIRouter

router = APIRouter(prefix="/mood", tags=["mood"])

# TODO: implement following the hikes router pattern in routers/hikes.py
#
#   POST /mood               — log a mood check-in
#   GET  /mood               — list (filter: tag, date)
#   GET  /mood/{id}          — single entry
#
# Models:  cairn/models/mood.py     (Mood)
# Schemas: cairn/schemas/mood.py    (MoodEntryCreate, MoodEntryRead, MoodDetails)
