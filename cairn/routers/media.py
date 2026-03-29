from fastapi import APIRouter

router = APIRouter(prefix="/media", tags=["media"])

# TODO: implement following the hikes router pattern in routers/hikes.py
#
#   POST /media              — log a book, film, TV show, podcast, or album
#   GET  /media              — list (filter: tag, date, media_type, status)
#   GET  /media/{id}         — single entry
#
# Models:  cairn/models/media.py    (Media, MediaType, MediaStatus)
# Schemas: cairn/schemas/media.py   (MediaEntryCreate, MediaEntryRead, MediaDetails)
