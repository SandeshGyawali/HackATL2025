from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime, timedelta
from app.database import db
import requests
from openai import OpenAI
import json

client = OpenAI()
router = APIRouter()


class SimulationRequest(BaseModel):
    product_id: str
    start_date: str  # YYYY-MM-DD format
    city: str


@router.post("/simulate")
def run_simulation(request: SimulationRequest):
    try:
        # Parse start date
        start_date = datetime.strptime(request.start_date, "%Y-%m-%d")

        # Get time estimate for the product
        response = requests.get(
            f"http://127.0.0.1:8000/estimate/time/{request.product_id}"
        )
        if response.status_code != 200:
            return {"error": "Could not get time estimate"}

        time_data = response.json()
        total_hours = time_data["total_estimated_hours"]

        # Calculate completion date (assuming 8 hours work per day)
        work_days = total_hours / 8
        completion_date = start_date + timedelta(days=work_days)

        # Get city names with available weather data
        response = requests.get(f"http://127.0.0.1:8000/weather")
        if response.status_code != 200:
            return {"error": "Could not get time estimate"}

        weather_data = response.json()
        weather_available_cities = [item["location"] for item in weather_data]
        nearest_city = find_nearest_city(request.city, weather_available_cities)
        print("Received nearest city= ", nearest_city)

        nearest_city_record = next(
            (item for item in weather_data if item["location"] == nearest_city), None
        )

        if not nearest_city_record:
            return {
                "error": f"No weather record found for nearest city: {nearest_city}"
            }

        nearest_city_id = nearest_city_record["_id"]

        print("Nearest city ID =", nearest_city_id)

        # Get weather forecast for the specified city
        response = requests.get(f"http://127.0.0.1:8000/weather/{nearest_city_id}")
        if response.status_code != 200:
            return {"error": "Could not get time estimate"}

        weather_info = response.json()

        # Generate recommendation
        recommendation = generate_recommendation(weather_info, completion_date)

        return {
            "product_id": request.product_id,
            "start_date": request.start_date,
            "city": request.city,
            "estimated_hours": total_hours,
            "work_days": round(work_days, 1),
            "completion_date": completion_date.strftime("%Y-%m-%d"),
            "weather": weather_info,
            "recommendation": recommendation.get("recommendation", ""),
            "delivery_recommendation": recommendation.get("delivery_recommendation", 1),
        }

    except Exception as e:
        return {"error": str(e)}


def find_nearest_city(city, weather_available_cities) -> str:
    prompt = f"""
    You are a helpful assistant that finds the closest matching city name.
    Available cities: {weather_available_cities}
    Requested city: "{city}"
    
    Reply with only the single best matching city name from the list above.
    """

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a precise text matching assistant."},
            {"role": "user", "content": prompt},
        ],
        temperature=0,
    )

    matched_city = completion.choices[0].message.content.strip()
    return matched_city


def generate_recommendation(weather_info, completion_date):
    prompt = f"""
    You are a logistics decision-making assistant.

    Context:
    - The company dispatches products for delivery.
    - Bad weather (rain, storms, heatwaves, snow, etc.) can delay or damage goods, reducing profit.
    - Good weather (sunny, mild, clear) is ideal for dispatch.

    Input:
    - Weather information: {weather_info}
    - Expected completion/delivery date: {completion_date}

    Task:
    1. Give a concise recommendation (maximum 3 sentences) about whether to proceed with delivery, delay it, or take preventive measures.
    2. Assign a delivery recommendation code based on the situation:
       - 0 → Highly recommended to proceed (good weather)
       - 1 → Neutral or uncertain (moderate weather)
       - 2 → Highly not recommended (bad or extreme weather)
    
    Output your response as valid JSON in the following format:
    {{
        "recommendation": "your short recommendation text here",
        "delivery_recommendation": <0 | 1 | 2>
    }}
    """

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a logistics and supply chain optimization assistant who provides short, clear advice.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
    )

    response_text = completion.choices[0].message.content.strip()

    try:
        result = json.loads(response_text)
    except Exception:
        # Fallback if the model response isn’t JSON
        result = {
            "recommendation": response_text,
            "delivery_recommendation": 1,  # Default to neutral
        }

    return result
