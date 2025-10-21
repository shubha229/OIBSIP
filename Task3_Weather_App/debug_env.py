# debug_env.py
from dotenv import load_dotenv
import os, requests

print("Working directory:", os.getcwd())
print("Python executable:", os.sys.executable)

load_dotenv()  # loads .env from cwd
key = os.getenv("WORLDWEATHER_API_KEY")
print("WORLDWEATHER_API_KEY:", repr(key))

# Try a direct request to WWO to see exact response (replace city if you like)
if key:
    url = "http://api.worldweatheronline.com/premium/v1/weather.ashx"
    params = {"key": key, "q": "London", "format": "json"}
    try:
        r = requests.get(url, params=params, timeout=10)
        print("HTTP status:", r.status_code)
        print("Response text (first 1000 chars):\n", r.text[:1000])
    except Exception as e:
        print("Request failed:", e)
else:
    print("No key found in environment.")
