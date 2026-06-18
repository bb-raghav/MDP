from urllib.parse import quote

import requests

from backend.services.cache import TTLCache


_cache = TTLCache(ttl_seconds=60 * 60)


def short_place_name(place):
    if not place:
        return ""

    if isinstance(place, str):
        return place.split(",")[0].strip()

    address = place.get("address", {}) or {}
    for key in ("city", "town", "village", "municipality", "county", "state_district", "state"):
        value = address.get(key)
        if value:
            return str(value).split(",")[0].strip()

    return str(place.get("name") or place.get("display_name") or "").split(",")[0].strip()


def geocode_city(city):
    cache_key = f"geocode:{city.strip().lower()}"
    cached = _cache.get(cache_key)
    if cached:
        return cached

    url = (
        "https://nominatim.openstreetmap.org/search"
        f"?q={quote(city)}&format=json&limit=1&addressdetails=1"
    )
    headers = {"User-Agent": "aqi-ai-project"}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
    except (requests.RequestException, ValueError):
        return {"error": "Geocoding service is unavailable"}

    if not data:
        return {"error": "City not found"}

    aqi_query = short_place_name(data[0]) or city.title()

    result = {
        "lat": float(data[0]["lat"]),
        "lon": float(data[0]["lon"]),
        "name": aqi_query,
        "display_name": data[0].get("display_name", city.title()),
        "aqi_query": aqi_query,
    }

    return _cache.set(cache_key, result)


def suggest_places(query, limit=5):
    cache_key = f"suggest:{query.strip().lower()}:{limit}"
    cached = _cache.get(cache_key)
    if cached:
        return cached

    url = (
        "https://nominatim.openstreetmap.org/search"
        f"?q={quote(query)}&format=json&limit={limit}&addressdetails=1"
    )
    headers = {"User-Agent": "aqi-ai-project"}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
    except (requests.RequestException, ValueError):
        return {"error": "geocoding failed"}

    suggestions = []
    for item in data:
        try:
            aqi_query = short_place_name(item)
            suggestions.append({
                "name": aqi_query or item.get("display_name"),
                "display_name": item.get("display_name"),
                "aqi_query": aqi_query,
                "lat": float(item.get("lat")),
                "lon": float(item.get("lon")),
            })
        except (TypeError, ValueError):
            continue

    return _cache.set(cache_key, {"suggestions": suggestions})
