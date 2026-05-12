from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {
        "message": "Air Quality Backend Running"
    }

@app.get("/aqi-points")
def get_points():

    return [
        {
            "name": "Central Bengaluru",
            "lat": 12.9716,
            "lon": 77.5946,
            "aqi": 78,
        },
        {
            "name": "Whitefield",
            "lat": 12.9698,
            "lon": 77.7500,
            "aqi": 52,
        },
        {
            "name": "Electronic City",
            "lat": 12.8456,
            "lon": 77.6603,
            "aqi": 91,
        },
    ]