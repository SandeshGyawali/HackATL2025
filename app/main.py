from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.product import router as product_router
from app.routes.chatbot import router as chatbot_router
from app.routes.simulation import router as simulation_router
from app.routes.weather import router as weather_router

app = FastAPI()

# ✅ Add this section
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or specify your frontend URL e.g. ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(product_router)
app.include_router(chatbot_router)
app.include_router(simulation_router)
app.include_router(weather_router)


@app.get("/")
def read_root():
    return {"message": "CrewAI setup successful!"}
