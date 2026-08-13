from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Wind forecast API is running"}

@app.get("/predict")
def predict(months: int = 24):
    # later: load the saved SARIMA model, run forecast, return real numbers
    fake_forecast = [45000 + i * 50 for i in range(months)]
    return {"months": months, "forecast": fake_forecast}