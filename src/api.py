from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import json
import numpy as np
import pandas as pd

# --- Load the trained model ---
model = joblib.load("models/solar_model.pkl")
with open("models/feature_columns.json") as f:
    feature_columns = json.load(f)

# --- Create the API ---
app = FastAPI(
    title="Solar Energy Forecaster",
    description="Predict sunlight from weather conditions"
)

# --- Define what inputs we expect ---
class WeatherInput(BaseModel):
    clouds: float        # Cloud cover in %  (0-100)
    temperature: float   # Temperature in °C
    humidity: float      # Humidity in %     (0-100)
    rain: float          # Rainfall in mm    (0+)
    hour: int            # Hour of day       (0-23)

# --- Health check endpoint ---
@app.get("/")
def home():
    return {"status": "running", "model": "Solar Forecaster"}

# --- Prediction endpoint ---
@app.post("/predict")
def predict(weather: WeatherInput):
    # Put the input into a table (DataFrame) with correct column order
    input_data = pd.DataFrame([{
        "clouds": weather.clouds,
        "temperature": weather.temperature,
        "humidity": weather.humidity,
        "rain": weather.rain,
        "hour": weather.hour,
    }])

    # Make prediction
    prediction = model.predict(input_data)[0]

    # Sunlight can't be negative
    prediction = max(0, float(prediction))

    return {
        "predicted_sunlight_wm2": round(prediction, 1),
        "input": weather.dict()
    }