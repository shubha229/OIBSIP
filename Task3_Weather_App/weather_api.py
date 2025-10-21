# weather_api.py
import os, requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("WORLDWEATHER_API_KEY")

BASE = "http://api.worldweatheronline.com/premium/v1/weather.ashx"

def get_weather(city, units="metric"):
    if not API_KEY:
        return {"error": "API key missing. Check your .env (WORLDWEATHER_API_KEY)."}

    params = {
        "key": API_KEY,
        "q": city,
        "format": "json",
        # you can request extra fields if desired:
        # "num_of_days": 1,
        # "tp": 1,
    }

    try:
        r = requests.get(BASE, params=params, timeout=10)
    except requests.RequestException as e:
        return {"error": f"Network error: {e}"}

    # If not 200, include server body so we can see detailed message
    if r.status_code != 200:
        return {"error": f"HTTP {r.status_code}: {r.text}"}

    try:
        js = r.json()
    except ValueError:
        return {"error": "Invalid JSON from API", "raw": r.text[:1000]}

    # If API sends errors in JSON, show them
    if "data" in js and "error" in js["data"]:
        # WWO often returns errors here
        errlist = js["data"]["error"]
        return {"error": " | ".join(e.get("msg", str(e)) for e in errlist), "raw": js}

    try:
        current = js["data"]["current_condition"][0]
        weather = {
            "city": city,
            "temp": current.get("temp_C") if units == "metric" else current.get("temp_F"),
            "humidity": current.get("humidity"),
            "condition": current.get("weatherDesc",[{}])[0].get("value"),
            # WWO returns full icon URL; we return last part for compatibility if needed
            "icon": current.get("weatherIconUrl",[{}])[0].get("value"),
            "wind_speed": current.get("windspeedKmph"),
        }
        return weather
    except Exception as e:
        return {"error": f"Parsing error: {e}", "raw": js}
