"""
gui.py - Tkinter front-end for weather_app

Requirements:
    pip install python-dotenv requests pillow

Place this file in the same folder as weather_api.py (which must provide get_weather(city, units)).
Also ensure your .env has:
    OPENWEATHER_API_KEY=your_api_key_here
"""

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
from io import BytesIO
import threading

# Import the get_weather function from your weather_api module
# weather_api.get_weather(city: str, units: "metric"|"imperial") -> dict
from weather_api import get_weather



# Example list of cities (you can expand this)
# CITIES = ["London", "New York", "Paris", "Tokyo", "Mumbai", "Sydney", "Berlin", "Moscow"]

class WeatherGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather App")
        self.units = "metric"  # default Celsius
        self.weather_icon = None  # keep a reference to prevent GC
        self.build_ui()

    def build_ui(self):
        # City input
        tk.Label(self.root, text="City:").grid(row=0, column=0, padx=5, pady=8, sticky="w")
        self.city_var = tk.StringVar()
        self.city_entry = tk.Entry(self.root, textvariable=self.city_var, width=20)
        self.city_entry.grid(row=0, column=1, padx=5, pady=8, sticky="w")
                
        # City drop-down
        #tk.Label(self.root, text="City:").grid(row=0, column=0, padx=5, pady=8, sticky="w")
        #self.city_var = tk.StringVar(value=CITIES[0])
        #self.city_menu = tk.OptionMenu(self.root, self.city_var, *CITIES)
        #self.city_menu.grid(row=0, column=1, padx=5, pady=8, sticky="w")

        # Units selector
        tk.Label(self.root, text="Units:").grid(row=0, column=2, padx=5, pady=8, sticky="w")
        self.unit_var = tk.StringVar(value="Celsius")
        unit_menu = tk.OptionMenu(self.root, self.unit_var, "Celsius", "Fahrenheit", command=self.change_units)
        unit_menu.grid(row=0, column=3, padx=5, pady=8, sticky="w")

        # Get weather button
        self.get_btn = tk.Button(self.root, text="Get Weather", command=self.on_get_weather)
        self.get_btn.grid(row=0, column=4, padx=10)

        # Output labels (information area)
        self.output = tk.Label(self.root, text="", justify="left", font=("Arial", 12), anchor="w")
        self.output.grid(row=1, column=0, columnspan=5, padx=10, pady=(6, 10), sticky="w")

        # Weather icon
        self.icon_label = tk.Label(self.root)
        self.icon_label.grid(row=2, column=0, columnspan=5, pady=(0, 10))

        # Make window a bit more compact and non-resizable
        self.root.resizable(False, False)
        self.root.geometry("")  # let geometry be natural

    def change_units(self, val):
        self.units = "metric" if val == "Celsius" else "imperial"

    def on_get_weather(self):
        """Called when Get Weather is clicked. Starts a background thread."""
        city = self.city_var.get().strip().title()
        if not city:
            messagebox.showwarning("Input Error", "Please enter a city name.")
            return

        # disable the button to prevent duplicate clicks
        self.get_btn.config(state="disabled", text="Loading...")
        self.output.config(text="Fetching weather...")
        self.icon_label.config(image="")

        # Start background thread
        thread = threading.Thread(target=self.fetch_weather_thread, args=(city, self.units), daemon=True)
        thread.start()

    def fetch_weather_thread(self, city, units):
        """Background thread: call API and then schedule update on main thread."""
        try:
            data = get_weather(city, units)
        except Exception as e:
            data = {"error": f"Unexpected error: {e}"}

        # Schedule UI update on main thread
        self.root.after(0, self.update_ui_after_fetch, data, units)

    def update_ui_after_fetch(self, data, units):
        """Update GUI widgets after the background fetch completes."""
        # Re-enable button
        self.get_btn.config(state="normal", text="Get Weather")

        if not data or "error" in data:
            err_msg = data.get("error") if isinstance(data, dict) else "Unknown error"
            self.output.config(text=f"Error: {err_msg}")
            messagebox.showerror("Weather Error", err_msg)
            self.icon_label.config(image="")
            return

        # Prepare display text
        unit_symbol = "°C" if units == "metric" else "°F"
        temp = data.get("temp", "N/A")
        humidity = data.get("humidity", "N/A")
        condition = data.get("condition", "N/A")
        wind_speed = data.get("wind_speed", None)

        # Convert wind speed: OpenWeather returns m/s; convert to mph for imperial.
        if wind_speed is None:
            wind_text = "N/A"
        else:
            if units == "metric":
                wind_text = f"{wind_speed} m/s"
            else:
                # convert m/s to mph: 1 m/s ≈ 2.23694 mph
                try:
                    mph = float(wind_speed) * 2.23694
                    wind_text = f"{round(mph, 2)} mph"
                except Exception:
                    wind_text = f"{wind_speed} (m/s)"

        info = (
            f"City: {data.get('city', 'N/A')}\n"
            f"Temperature: {temp}{unit_symbol}\n"
            f"Humidity: {humidity}%\n"
            f"Condition: {condition}\n"
            f"Wind Speed: {wind_text}"
        )
        self.output.config(text=info)

        # Fetch and display the icon (non-blocking small request)
        icon_code = data.get("icon")
        if icon_code:
            try:
                icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
                resp = requests.get(icon_url, timeout=8)
                resp.raise_for_status()
                img = Image.open(BytesIO(resp.content))
                img = img.resize((100, 100), Image.ANTIALIAS)
                self.weather_icon = ImageTk.PhotoImage(img)
                self.icon_label.config(image=self.weather_icon)
            except Exception:
                self.icon_label.config(image="")
        else:
            self.icon_label.config(image="")

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherGUI(root)
    root.mainloop()
