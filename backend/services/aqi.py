from urllib.parse import quote

import requests

from backend.services.cache import TTLCache


_cache = TTLCache(ttl_seconds=5 * 60)


def get_category(aqi):
    if aqi <= 50:
        return "Good"
    if aqi <= 100:
        return "Moderate"
    if aqi <= 150:
        return "Poor"
    return "Severe"


def fetch_live_aqi(city, token):
    city = city.strip().split(",")[0].strip()

    if not token:
        return {"error": "WAQI_API_KEY environment variable is not set"}

    cache_key = f"live-aqi:{city.lower()}"
    cached = _cache.get(cache_key)
    if cached:
        return cached

    url = f"https://api.waqi.info/feed/{quote(city)}/?token={token}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
    except (requests.RequestException, ValueError):
        return {"error": "WAQI service is unavailable"}

    if data.get("status") != "ok":
        return {"error": f"WAQI could not find {city}"}

    station = data.get("data", {})
    iaqi = station.get("iaqi", {})
    temperature = round(iaqi.get("t", {}).get("v", 30), 1)

    result = {
        "live_aqi": station.get("aqi", 0),
        "pm25": iaqi.get("pm25", {}).get("v", 0),
        "pm10": iaqi.get("pm10", {}).get("v", 0),
        "no2": iaqi.get("no2", {}).get("v", 0),
        "so2": iaqi.get("so2", {}).get("v", 0),
        "co": iaqi.get("co", {}).get("v", 0),
        "temperature": temperature,
        "humidity": iaqi.get("h", {}).get("v", 60),
        "pressure": iaqi.get("p", {}).get("v", 1008),
        "wind_speed": iaqi.get("w", {}).get("v", 5),
        "apparent_temperature": temperature,
        "station_name": station.get("city", {}).get("name", city),
        "status": get_category(station.get("aqi", 0)),
    }

    return _cache.set(cache_key, result)
