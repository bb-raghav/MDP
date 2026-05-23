import pandas as pd
import joblib
import os

MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "saved",
    "aqi_regression_model.pkl"
)


# =========================
# LOAD MODEL
# =========================

print("\nLoading AQI model...\n")

model = joblib.load(MODEL_PATH)


# =========================
# AQI CATEGORY
# =========================

def get_aqi_category(aqi):
    if aqi <= 50:
        return "Good"
    elif aqi <= 100:
        return "Moderate"
    elif aqi <= 150:
        return "Poor"
    else:
        return "Very Poor"


# =========================
# PREDICT FUNCTION
# =========================

def predict_aqi(input_data):

    df = pd.DataFrame([input_data])


    prediction = model.predict(df)[0]

    prediction = float(

        round(
            prediction,
            2
        )
    )


    category = get_aqi_category(
        prediction
    )


    return {

        "predicted_aqi":
            prediction,

        "category":
            category
    }


# =========================
# TEST
# =========================

if __name__ == "__main__":

    sample_input = {

        "pm2_5": 80,
        "pm10": 130,
        "no2": 40,
        "so2": 20,
        "co": 2,

        "temperature": 30,
        "humidity": 70,
        "pressure": 1008,
        "wind_speed": 8,
        "apparent_temperature": 33,

        "year": 2025,
        "month": 5,
        "day": 13,
        "weekday": 1,

        "city_encoded": 0
    }


    result = predict_aqi(
        sample_input
    )


    print("\nPrediction Result:\n")

    print(result)