# 🌦️ Weather Forecasting Application (Python & Tkinter)

A beginner-friendly, modular desktop weather forecasting application built with **Python**, **Tkinter**, and the free **Open-Meteo API**.

Users can search for any city worldwide to view real-time current weather metrics (temperature, humidity, wind speed, feels-like temperature) and a clean 7-day weather forecast with precipitation probability and temperature ranges.

---

## 🌟 Key Features

1. **City Search & Geocoding**:
   - Converts any city name into latitude & longitude coordinates using the free Open-Meteo Geocoding API.
   - Automatically displays the formatted location name, administrative region, and country (e.g., *Pune, Maharashtra, India*).
2. **Current Weather Overview**:
   - Real-time temperature (°C).
   - Weather condition text and visual weather emoji (e.g., *Partly Cloudy ⛅*).
   - "Feels like" apparent temperature.
   - Relative humidity (%).
   - Wind speed (km/h).
3. **7-Day Weather Forecast**:
   - 7 consecutive day breakdown (starting from *Today* through the upcoming 6 days).
   - Daily maximum and minimum temperatures.
   - Weather condition description and icon for each day.
   - Maximum precipitation (rain) probability (%).
4. **Smooth & Responsive GUI**:
   - Built with Python's standard `tkinter` and `ttk` library.
   - **Non-blocking Background Threading**: Network requests execute asynchronously so the application never freezes or shows "Not Responding" while fetching weather data.
   - Press <kbd>Enter</kbd> or click the "Get Weather" button to search.
5. **Robust Error Handling**:
   - Handles empty city searches with a clear validation prompt.
   - Gracefully handles unknown or misspelled cities.
   - Handles internet disconnects, timeouts, or API errors without crashing.
6. **No Paid APIs / No API Keys Required**:
   - Uses Open-Meteo's completely free, open-access meteorological endpoints.

---

## 📁 Project Structure

```text
WeatherForecast/
│
├── main.py            # Main entry point to launch the application
├── weather_api.py     # API client handling geocoding, weather requests, and WMO codes
├── gui.py             # Tkinter desktop GUI layout, styling, and event handling
├── requirements.txt   # Project dependencies (requests library)
└── README.md          # Comprehensive documentation and guide
```

### Module Breakdown

| File | Purpose |
| :--- | :--- |
| `weather_api.py` | Contains `get_coordinates(city_name)` to convert city names to coordinates, and `get_weather_data(lat, lon)` to retrieve current conditions and 7-day forecasts from Open-Meteo. Also translates WMO weather codes into plain English and emojis. |
| `gui.py` | Defines the `WeatherApp` class. Manages the visual interface, input fields, cards, and executes network requests in background daemon threads so the UI stays smooth. |
| `main.py` | The entry point script that configures the Tkinter root window, centers it on the screen, initializes `WeatherApp`, and starts the main event loop. |
| `requirements.txt` | Lists external Python libraries needed for the project (`requests`). |

---

## 🛠️ Prerequisites

- **Python 3.8 or higher** installed on your computer.
- Python `pip` package manager.
- An active internet connection (to fetch live weather data).

---

## 🚀 Installation & Setup Guide

### Step 1: Open the Project in VS Code or Terminal

Open your terminal or VS Code and navigate to the `WeatherForecast` directory:

```bash
cd WeatherForecast
```

### Step 2: (Optional but Recommended) Create a Virtual Environment

Creating a virtual environment keeps your project packages isolated:

**On Windows:**
```powershell
python -m venv venv
.\venv\Scripts\activate
```

**On macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Required Dependencies

Install the `requests` library:

```bash
pip install -r requirements.txt
```

*(Alternatively: `python -m pip install -r requirements.txt`)*

---

## ▶️ How to Run the Application

Execute `main.py` using Python:

```bash
python main.py
```

### Quick Usage:
1. When launched, the application opens and automatically loads weather for the default city (**Pune**).
2. Type any other city into the input box (e.g. *Tokyo*, *London*, *New York*, *Sydney*, *Berlin*, *Mumbai*).
3. Click **"Get Weather"** or press <kbd>Enter</kbd>.
4. Watch the status bar update and view current conditions along with the 7-day forecast.

---

## 🧪 Testing the Modules Separately

You can test individual modules directly from the command line to understand how data flows:

### Test the Weather API Alone:
```bash
python -c "from weather_api import get_coordinates, get_weather_data; loc = get_coordinates('Pune'); print(loc); data = get_weather_data(loc['latitude'], loc['longitude']); print('Temp:', data['current']['temperature'], 'Condition:', data['current']['condition'])"
```

---

## 🌐 How Open-Meteo API Works

This application utilizes two free endpoints provided by [Open-Meteo](https://open-meteo.com/):

1. **Geocoding API**:
   - Endpoint: `https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json`
   - Maps user-entered city names to exact decimal coordinates (`latitude`, `longitude`).
2. **Forecast API**:
   - Endpoint: `https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=...&daily=...&timezone=auto`
   - Returns hourly and daily weather metrics along with **WMO Weather Interpretation Codes** (e.g., Code `0` = Clear Sky, Code `61` = Slight Rain, Code `95` = Thunderstorm).

---

## 💡 Suggestions for Future Improvements

Want to take this project further? Here are great beginner-to-intermediate enhancements you can add:

1. **Temperature Unit Toggle (°C / °F)**:
   - Add a toggle switch or dropdown to switch between Celsius and Fahrenheit.
2. **Hourly Weather Forecast**:
   - Display a horizontal scrolling row showing temperatures for the next 24 hours.
3. **Recent Search History / Favorites**:
   - Save frequently searched cities in a local JSON file or SQLite database for quick 1-click access.
4. **Dark / Light Theme Toggle**:
   - Add a button in the header to switch between a crisp light mode and a modern dark mode.
5. **Weather Alerts & Sunrise / Sunset**:
   - Open-Meteo also provides daily `sunrise` and `sunset` times as well as UV index.
6. **Packaging into an Executable (.exe)**:
   - Use `pyinstaller --onefile --windowed main.py` to create a standalone desktop app that can run on any Windows computer without installing Python!

---

## 📄 License
This project is open-source and free to use for learning, educational, and personal purposes.
