from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

from data_loader import load_wind_series, train_test_split
from model import load_model, forecast

app = FastAPI(title="US Wind Generation Forecast API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Loaded once at startup
series = load_wind_series()
train, test = train_test_split(series)
fitted_model = load_model()  # expects wind_model.pkl to exist — see train_model.py


@app.get("/")
def home():
    return {"message": "Wind forecast API is running"}


@app.get("/history")
def history():
    return {
        "dates": [d.strftime("%Y-%m") for d in series.index],
        "values": series.round(2).tolist(),
    }


@app.get("/predict")
def predict(months: int = 24):
    last_date = series.index[-1]
    start = (last_date + pd.DateOffset(months=1)).strftime("%Y-%m-%d")
    result = forecast(fitted_model, steps=months, start_date=start)
    return {
        "months": months,
        "dates": [d.strftime("%Y-%m") for d in result.index],
        "forecast": result["forecast"].round(2).tolist(),
        "lower_95": result["lower_95"].round(2).tolist(),
        "upper_95": result["upper_95"].round(2).tolist(),
    }