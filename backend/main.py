import os
from dotenv import load_dotenv
import requests
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()  # ✅ This loads .env variables

API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")
print("Loaded API Key:", API_KEY)  # 👈 Test if it's loading

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/weather")
def get_weather(city: str = Query(...)):
    if not API_KEY:
        return {"error": "API key not loaded"}

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()

    if "main" not in data:
        return {"error": "City not found", "details": data}

    return {
        "city": city,
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "description": data["weather"][0]["description"]
    }
