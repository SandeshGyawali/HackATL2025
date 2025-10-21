from fastapi import APIRouter, HTTPException
from bson import ObjectId
from app.database import db

router = APIRouter()


@router.get("/weather")
async def get_all_weather():
    weather_data = db["weather_data"]
    cursor = weather_data.find({}, {"_id": 1, "location": 1})
    results = []
    async for doc in cursor:
        # Convert ObjectId to string for JSON serialization
        doc["_id"] = str(doc["_id"])
        results.append(doc)
    return results


@router.get("/weather/{weather_id}")
async def get_weather(weather_id: str):
    weather_data = db["weather_data"]

    try:
        object_id = ObjectId(weather_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid weather ID format")

    record = await weather_data.find_one({"_id": object_id})  # <-- await here

    if not record:
        raise HTTPException(status_code=404, detail="Weather record not found")

    record["_id"] = str(record["_id"])
    return record
