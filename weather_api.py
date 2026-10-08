"""
weather_api.py - Weather and Geocoding API Module
-------------------------------------------------
Handles network requests to the free Open-Meteo APIs:
1. Geocoding API: Converts a city name into latitude & longitude coordinates.
2. Weather Forecast API: Retrieves real-time current weather and a 7-day forecast.
3. Translates WMO weather codes into human-readable descriptions and emojis.
"""

from datetime import datetime
import requests

# Open-Meteo API Endpoints
GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

# Mapping WMO Weather Interpretation Codes to (Description, Emoji)
# Reference: https://open-meteo.com/en/docs
WEATHER_CODES = {
    0: ("Clear Sky", "☀️"),
    1: ("Mainly Clear", "🌤️"),
    2: ("Partly Cloudy", "⛅"),
    3: ("Overcast", "☁️"),
    45: ("Foggy", "🌫️"),
    48: ("Depositing Rime Fog", "🌫️"),
    51: ("Light Drizzle", "🌦️"),
    53: ("Moderate Drizzle", "🌦️"),
    55: ("Dense Drizzle", "🌧️"),
    56: ("Light Freezing Drizzle", "🌧️❄️"),
    57: ("Dense Freezing Drizzle", "🌧️❄️"),
    61: ("Slight Rain", "🌦️"),
    63: ("Moderate Rain", "🌧️"),
    65: ("Heavy Rain", "🌧️"),
    66: ("Light Freezing Rain", "🌨️"),
    67: ("Heavy Freezing Rain", "🌨️"),
    71: ("Slight Snow Fall", "🌨️"),
    73: ("Moderate Snow Fall", "🌨️"),
    75: ("Heavy Snow Fall", "❄️"),
    77: ("Snow Grains", "❄️"),
    80: ("Slight Rain Showers", "🌦️"),
    81: ("Moderate Rain Showers", "🌧️"),
    82: ("Violent Rain Showers", "⛈️"),
    85: ("Slight Snow Showers", "🌨️"),
    86: ("Heavy Snow Showers", "❄️"),
    95: ("Thunderstorm", "⛈️"),
    96: ("Thunderstorm with Slight Hail", "⛈️"),
    99: ("Thunderstorm with Heavy Hail", "⛈️"),
}


def get_weather_description(code: int) -> tuple[str, str]:
    """
    Translates a WMO weather code into a readable text and emoji icon.
    Defaults to ('Unknown', '❓') if the code is not in the dictionary.
    """
    return WEATHER_CODES.get(code, ("Unknown", "❓"))


def get_coordinates(city_name: str) -> dict:
    """
    Converts a user-provided city name into geographical coordinates (lat/lon).

    Returns:
        dict: {
            'name': 'Pune',
            'display_name': 'Pune, Maharashtra, India',
            'latitude': 18.51957,
            'longitude': 73.85535,
            'country': 'India',
            'timezone': 'Asia/Kolkata'
        }

    Raises:
        ValueError: If city is empty, whitespace, or not found.
        ConnectionError: If network request fails or times out.
    """
    clean_city = city_name.strip()
    if not clean_city:
        raise ValueError("Please enter a city name.")

    params = {
        "name": clean_city,
        "count": 1,
        "language": "en",
        "format": "json"
    }

    try:
        response = requests.get(GEOCODING_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.Timeout:
        raise ConnectionError("Geocoding request timed out. Please check your internet connection.")
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"Network error while searching for city: {e}")
    except ValueError:
        raise ValueError("Invalid response received from Geocoding service.")

    # Check if any location was returned
    results = data.get("results")
    if not results:
        raise ValueError(f"Could not find any city named '{clean_city}'. Please verify the spelling.")

    top_result = results[0]

    # Build a friendly display name (e.g., "Pune, Maharashtra, India")
    name_parts = [top_result.get("name")]
    admin1 = top_result.get("admin1")
    country = top_result.get("country")
    if admin1 and admin1 != top_result.get("name"):
        name_parts.append(admin1)
    if country:
        name_parts.append(country)

    display_name = ", ".join(name_parts)

    return {
        "name": top_result.get("name", clean_city),
        "display_name": display_name,
        "latitude": top_result.get("latitude"),
        "longitude": top_result.get("longitude"),
        "country": country or "",
        "timezone": top_result.get("timezone", "auto")
    }


def get_weather_data(latitude: float, longitude: float) -> dict:
    """
    Fetches real-time current weather and 7-day forecast for the given coordinates.

    Returns:
        dict: {
            'current': {
                'temperature': 28.5,
                'feels_like': 30.1,
                'humidity': 65,
                'wind_speed': 12.0,
                'condition': 'Partly Cloudy',
                'icon': '⛅',
                'time': '2026-10-08 18:30'
            },
            'forecast': [
                {
                    'date': '2026-10-08',
                    'day_name': 'Today',
                    'temp_max': 32.0,
                    'temp_min': 19.5,
                    'condition': 'Clear Sky',
                    'icon': '☀️',
                    'precipitation_prob': 10
                },
                ... (7 items total)
            ]
        }

    Raises:
        ConnectionError: If network request fails or times out.
        ValueError: If API response cannot be parsed.
    """
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": [
            "temperature_2m",
            "relative_humidity_2m",
            "apparent_temperature",
            "weather_code",
            "wind_speed_10m"
        ],
        "daily": [
            "weather_code",
            "temperature_2m_max",
            "temperature_2m_min",
            "precipitation_probability_max"
        ],
        "timezone": "auto",
        "forecast_days": 7
    }

    try:
        response = requests.get(FORECAST_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.Timeout:
        raise ConnectionError("Weather forecast request timed out. Please try again.")
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"Network error while fetching weather data: {e}")
    except ValueError:
        raise ValueError("Invalid response received from Weather service.")

    # 1. Parse Current Weather
    current_raw = data.get("current", {})
    current_code = current_raw.get("weather_code", -1)
    condition_text, condition_icon = get_weather_description(current_code)

    current_data = {
        "temperature": round(current_raw.get("temperature_2m", 0.0), 1),
        "feels_like": round(current_raw.get("apparent_temperature", 0.0), 1),
        "humidity": current_raw.get("relative_humidity_2m", 0),
        "wind_speed": round(current_raw.get("wind_speed_10m", 0.0), 1),
        "condition": condition_text,
        "icon": condition_icon,
        "time": current_raw.get("time", "").replace("T", " ")
    }

    # 2. Parse 7-Day Forecast
    daily_raw = data.get("daily", {})
    dates = daily_raw.get("time", [])
    codes = daily_raw.get("weather_code", [])
    max_temps = daily_raw.get("temperature_2m_max", [])
    min_temps = daily_raw.get("temperature_2m_min", [])
    precip_probs = daily_raw.get("precipitation_probability_max", [])

    forecast_list = []
    today_str = datetime.now().strftime("%Y-%m-%d")

    for i in range(len(dates)):
        date_str = dates[i]
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            # If the forecast date matches today, label as "Today", otherwise day name
            if date_str == today_str:
                day_name = "Today"
            else:
                day_name = dt.strftime("%A")
            formatted_date = dt.strftime("%b %d")
        except Exception:
            day_name = date_str
            formatted_date = date_str

        code = codes[i] if i < len(codes) else -1
        day_cond, day_icon = get_weather_description(code)
        t_max = round(max_temps[i], 1) if i < len(max_temps) and max_temps[i] is not None else 0.0
        t_min = round(min_temps[i], 1) if i < len(min_temps) and min_temps[i] is not None else 0.0
        p_prob = precip_probs[i] if i < len(precip_probs) and precip_probs[i] is not None else 0

        forecast_list.append({
            "date": formatted_date,
            "day_name": day_name,
            "temp_max": t_max,
            "temp_min": t_min,
            "condition": day_cond,
            "icon": day_icon,
            "precipitation_prob": p_prob
        })

    return {
        "current": current_data,
        "forecast": forecast_list
    }
