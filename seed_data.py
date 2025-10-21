import asyncio
from app.database import db

# === NASA Product Data ===
products = [
    {
        "_id": "product_3",
        "name": "NASA Advanced Lithium-Sulfur Battery",
        "description": "Lightweight, high-energy-density battery for spacecraft and rovers. Based on NASA Glenn Research Center prototypes.",
    },
    {
        "_id": "product_4",
        "name": "NASA Portable Solar Charging Array",
        "description": "Foldable solar panel charger designed for use on Mars surface missions and remote power setups.",
    },
    {
        "_id": "product_5",
        "name": "NASA Carbon Fiber Composite Panel",
        "description": "High-strength, low-mass carbon fiber panel used in spacecraft fuselage and payload structures.",
    },
]

# === Production Steps ===
production_steps = [
    # Lithium-Sulfur Battery
    {
        "_id": "step_5",
        "product_id": "product_3",
        "name": "Cathode Material Synthesis",
        "description": "Synthesize sulfur-carbon composite cathode with nanostructured carbon matrix.",
    },
    {
        "_id": "step_6",
        "product_id": "product_3",
        "name": "Cell Assembly",
        "description": "Assemble anode, cathode, and separator in dry room conditions.",
    },
    {
        "_id": "step_7",
        "product_id": "product_3",
        "name": "Battery Pack Integration",
        "description": "Integrate cells into modules and perform electrical balancing and thermal management.",
    },
    # Portable Solar Charger
    {
        "_id": "step_8",
        "product_id": "product_4",
        "name": "Photovoltaic Panel Fabrication",
        "description": "Manufacture flexible GaAs (Gallium Arsenide) solar cells for high efficiency under Martian sunlight.",
    },
    {
        "_id": "step_9",
        "product_id": "product_4",
        "name": "Frame Assembly",
        "description": "Assemble lightweight aluminum frame with unfolding hinges and wiring harness.",
    },
    {
        "_id": "step_10",
        "product_id": "product_4",
        "name": "Power Regulation Circuit Integration",
        "description": "Integrate MPPT (maximum power point tracking) converter and battery interface.",
    },
    # Carbon Fiber Composite Panel
    {
        "_id": "step_11",
        "product_id": "product_5",
        "name": "Prepreg Layup",
        "description": "Lay up carbon fiber prepreg sheets on mold tool using automated fiber placement system.",
    },
    {
        "_id": "step_12",
        "product_id": "product_5",
        "name": "Autoclave Curing",
        "description": "Cure the composite at 180°C under 7 bar pressure to achieve aerospace-grade bonding.",
    },
    {
        "_id": "step_13",
        "product_id": "product_5",
        "name": "Panel Finishing & Inspection",
        "description": "Trim edges, apply surface coating, and perform ultrasonic NDI inspection.",
    },
]

# === Step Time Estimates (approx. NASA engineering production data) ===
production_step_times = [
    {"_id": "time_5", "step_id": "step_5", "estimated_hours": 36},
    {"_id": "time_6", "step_id": "step_6", "estimated_hours": 48},
    {"_id": "time_7", "step_id": "step_7", "estimated_hours": 24},
    {"_id": "time_8", "step_id": "step_8", "estimated_hours": 30},
    {"_id": "time_9", "step_id": "step_9", "estimated_hours": 16},
    {"_id": "time_10", "step_id": "step_10", "estimated_hours": 20},
    {"_id": "time_11", "step_id": "step_11", "estimated_hours": 40},
    {"_id": "time_12", "step_id": "step_12", "estimated_hours": 18},
    {"_id": "time_13", "step_id": "step_13", "estimated_hours": 10},
]

# === Materials per Step ===
production_step_materials = [
    # Battery
    {
        "_id": "material_6",
        "step_id": "step_5",
        "name": "Sulfur Powder (99.9%)",
        "quantity": 15,
    },
    {
        "_id": "material_7",
        "step_id": "step_5",
        "name": "Carbon Nanotubes",
        "quantity": 5,
    },
    {
        "_id": "material_8",
        "step_id": "step_6",
        "name": "Lithium Metal Foil",
        "quantity": 12,
    },
    {
        "_id": "material_9",
        "step_id": "step_7",
        "name": "Battery Management System Board",
        "quantity": 2,
    },
    # Solar Charger
    {
        "_id": "material_10",
        "step_id": "step_8",
        "name": "Gallium Arsenide Solar Cells",
        "quantity": 20,
    },
    {
        "_id": "material_11",
        "step_id": "step_9",
        "name": "Aluminum Alloy Frame",
        "quantity": 5,
    },
    {
        "_id": "material_12",
        "step_id": "step_10",
        "name": "MPPT Converter Module",
        "quantity": 2,
    },
    # Carbon Fiber Panel
    {
        "_id": "material_13",
        "step_id": "step_11",
        "name": "Carbon Fiber Prepreg Rolls",
        "quantity": 10,
    },
    {"_id": "material_14", "step_id": "step_12", "name": "Epoxy Resin", "quantity": 8},
    {
        "_id": "material_15",
        "step_id": "step_13",
        "name": "Surface Coating Compound",
        "quantity": 4,
    },
]

# === Material Prices (based on aerospace-grade component costs in USD) ===
production_step_material_prices = [
    {"_id": "price_6", "material_id": "material_6", "unit_price": 80.0},  # sulfur
    {"_id": "price_7", "material_id": "material_7", "unit_price": 250.0},  # CNT
    {
        "_id": "price_8",
        "material_id": "material_8",
        "unit_price": 500.0,
    },  # lithium foil
    {"_id": "price_9", "material_id": "material_9", "unit_price": 1200.0},  # BMS board
    {"_id": "price_10", "material_id": "material_10", "unit_price": 400.0},  # GaAs cell
    {
        "_id": "price_11",
        "material_id": "material_11",
        "unit_price": 150.0,
    },  # aluminum frame
    {"_id": "price_12", "material_id": "material_12", "unit_price": 600.0},  # MPPT
    {
        "_id": "price_13",
        "material_id": "material_13",
        "unit_price": 900.0,
    },  # carbon prepreg
    {
        "_id": "price_14",
        "material_id": "material_14",
        "unit_price": 300.0,
    },  # epoxy resin
    {"_id": "price_15", "material_id": "material_15", "unit_price": 250.0},  # coating
]

weather_data = [
    {
        "date": "2025-10-01",
        "location": "Los Angeles, CA",
        "temperature_c": 26,
        "humidity_percent": 45,
        "condition": "Sunny",
        "description": "Clear skies with mild temperatures throughout the day.",
        "severity": "positive",
        "wind_speed_kmh": 12,
        "precipitation_mm": 0,
    },
    {
        "date": "2025-10-02",
        "location": "Miami, FL",
        "temperature_c": 31,
        "humidity_percent": 75,
        "condition": "Humid and Partly Cloudy",
        "description": "Warm and sticky with occasional sunshine.",
        "severity": "positive",
        "wind_speed_kmh": 15,
        "precipitation_mm": 2,
    },
    {
        "date": "2025-10-03",
        "location": "Seattle, WA",
        "temperature_c": 14,
        "humidity_percent": 90,
        "condition": "Light Rain",
        "description": "Occasional drizzle with overcast skies.",
        "severity": "neutral",
        "wind_speed_kmh": 8,
        "precipitation_mm": 6,
    },
    {
        "date": "2025-10-04",
        "location": "Chicago, IL",
        "temperature_c": 10,
        "humidity_percent": 60,
        "condition": "Windy",
        "description": "Cool and windy conditions but generally clear.",
        "severity": "positive",
        "wind_speed_kmh": 35,
        "precipitation_mm": 0,
    },
    {
        "date": "2025-10-05",
        "location": "Houston, TX",
        "temperature_c": 34,
        "humidity_percent": 70,
        "condition": "Heatwave",
        "description": "Extreme heat with persistent sun exposure.",
        "severity": "negative",
        "wind_speed_kmh": 10,
        "precipitation_mm": 0,
    },
    {
        "date": "2025-10-06",
        "location": "Denver, CO",
        "temperature_c": 18,
        "humidity_percent": 30,
        "condition": "Sunny and Cool",
        "description": "Pleasant fall day with clear skies.",
        "severity": "positive",
        "wind_speed_kmh": 9,
        "precipitation_mm": 0,
    },
    {
        "date": "2025-10-07",
        "location": "New York, NY",
        "temperature_c": 12,
        "humidity_percent": 65,
        "condition": "Heavy Rain",
        "description": "Intense rainfall for 2 days causing minor flooding.",
        "severity": "negative",
        "wind_speed_kmh": 20,
        "precipitation_mm": 85,
    },
    {
        "date": "2025-10-08",
        "location": "Boston, MA",
        "temperature_c": 9,
        "humidity_percent": 80,
        "condition": "Cold and Foggy",
        "description": "Low visibility in the morning, chilly breeze.",
        "severity": "neutral",
        "wind_speed_kmh": 10,
        "precipitation_mm": 3,
    },
    {
        "date": "2025-10-09",
        "location": "Las Vegas, NV",
        "temperature_c": 29,
        "humidity_percent": 20,
        "condition": "Sunny",
        "description": "Hot but dry — perfect for outdoor activities.",
        "severity": "positive",
        "wind_speed_kmh": 5,
        "precipitation_mm": 0,
    },
    {
        "date": "2025-10-10",
        "location": "Portland, OR",
        "temperature_c": 11,
        "humidity_percent": 85,
        "condition": "Moderate Rain",
        "description": "Steady rain all afternoon with cooler temps.",
        "severity": "neutral",
        "wind_speed_kmh": 12,
        "precipitation_mm": 22,
    },
    {
        "date": "2025-10-11",
        "location": "Phoenix, AZ",
        "temperature_c": 41,
        "humidity_percent": 18,
        "condition": "Extreme Heat",
        "description": "Dangerously high temperature, heat advisory issued.",
        "severity": "negative",
        "wind_speed_kmh": 7,
        "precipitation_mm": 0,
    },
    {
        "date": "2025-10-12",
        "location": "San Francisco, CA",
        "temperature_c": 20,
        "humidity_percent": 60,
        "condition": "Partly Cloudy",
        "description": "Cool breeze with scattered clouds, comfortable weather.",
        "severity": "positive",
        "wind_speed_kmh": 14,
        "precipitation_mm": 0,
    },
    {
        "date": "2025-10-13",
        "location": "Atlanta, GA",
        "temperature_c": 23,
        "humidity_percent": 50,
        "condition": "Mild and Pleasant",
        "description": "Perfect day with moderate warmth and clear skies.",
        "severity": "positive",
        "wind_speed_kmh": 11,
        "precipitation_mm": 0,
    },
    {
        "date": "2025-10-14",
        "location": "Dallas, TX",
        "temperature_c": 17,
        "humidity_percent": 40,
        "condition": "Cool and Breezy",
        "description": "Light winds and comfortable temperatures.",
        "severity": "positive",
        "wind_speed_kmh": 18,
        "precipitation_mm": 0,
    },
    {
        "date": "2025-10-15",
        "location": "Minneapolis, MN",
        "temperature_c": -3,
        "humidity_percent": 78,
        "condition": "Snowstorm",
        "description": "Heavy snow accumulation disrupting traffic.",
        "severity": "negative",
        "wind_speed_kmh": 40,
        "precipitation_mm": 50,
    },
    {
        "date": "2025-10-16",
        "location": "San Diego, CA",
        "temperature_c": 24,
        "humidity_percent": 55,
        "condition": "Clear and Breezy",
        "description": "Calm weather, slight winds from the ocean.",
        "severity": "positive",
        "wind_speed_kmh": 13,
        "precipitation_mm": 0,
    },
    {
        "date": "2025-10-17",
        "location": "New Orleans, LA",
        "temperature_c": 27,
        "humidity_percent": 88,
        "condition": "Thunderstorm",
        "description": "Lightning and heavy rain lasting several hours.",
        "severity": "negative",
        "wind_speed_kmh": 28,
        "precipitation_mm": 60,
    },
    {
        "date": "2025-10-18",
        "location": "Anchorage, AK",
        "temperature_c": -5,
        "humidity_percent": 85,
        "condition": "Light Snow",
        "description": "Light snow flurries, no major accumulation.",
        "severity": "neutral",
        "wind_speed_kmh": 10,
        "precipitation_mm": 5,
    },
    {
        "date": "2025-10-19",
        "location": "Tampa, FL",
        "temperature_c": 28,
        "humidity_percent": 65,
        "condition": "Sunny",
        "description": "Warm tropical day with low humidity — beach weather.",
        "severity": "positive",
        "wind_speed_kmh": 9,
        "precipitation_mm": 0,
    },
    {
        "date": "2025-10-20",
        "location": "Detroit, MI",
        "temperature_c": 6,
        "humidity_percent": 70,
        "condition": "Cold Rain",
        "description": "Continuous rainfall with low temperatures and strong winds.",
        "severity": "negative",
        "wind_speed_kmh": 30,
        "precipitation_mm": 45,
    },
]


# === Async Seeder ===
async def seed():
    # await db["product"].insert_many(products)
    # await db["production_step"].insert_many(production_steps)
    # await db["production_step_time"].insert_many(production_step_times)
    # await db["production_step_material"].insert_many(production_step_materials)
    # await db["production_step_material_price"].insert_many(
    #     production_step_material_prices
    # )
    await db["weather_data"].insert_many(weather_data)
    print("✅ NASA product dataset seeded successfully!")


if __name__ == "__main__":
    asyncio.run(seed())
