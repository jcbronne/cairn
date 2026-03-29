from fastapi import APIRouter

router = APIRouter(prefix="/workouts", tags=["workouts"])

# TODO: implement following the hikes router pattern in routers/hikes.py
#
#   POST /workouts           — log a workout
#   GET  /workouts           — list (filter: tag, date, workout_type)
#   GET  /workouts/{id}      — single entry
#
# Models:  cairn/models/workout.py  (Workout)
# Schemas: cairn/schemas/workout.py (WorkoutEntryCreate, WorkoutEntryRead, WorkoutDetails)
