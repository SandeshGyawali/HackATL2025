import motor.motor_asyncio
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")

if not MONGO_URI or not MONGO_DB_NAME:
    raise ValueError("❌ Missing MONGO_URI or MONGO_DB_NAME in .env file")

client = motor.motor_asyncio.AsyncIOMotorClient(
    MONGO_URI,
    tls=True,
    tlsAllowInvalidCertificates=True
)
db = client[MONGO_DB_NAME]  # safe now because we validated

print(f"✅ Connected to MongoDB database: {MONGO_DB_NAME}")
