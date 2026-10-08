"""
gui.py - Tkinter Graphical User Interface
-----------------------------------------
Provides a clean, beginner-friendly desktop interface for the Weather Forecasting app.
Features:
- Search bar with Enter key binding
- Non-blocking API requests via threading
- Live status and validation error messages
- Current weather overview card
- 7-Day weather forecast cards
"""

import threading
import tkinter as tk
from tkinter import ttk

from weather_api import get_coordinates, get_weather_data


class WeatherApp:
    """
    Main Application GUI Class.
    Manages the Tkinter window, widgets, styling, and data rendering.
    """

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Weather Forecast Application")
        self.root.geometry("640x780")
        self.root.minsize(580, 680)

        # Color Theme (Clean Modern Slate Palette)
        self.BG_COLOR = "#f1f5f9"         # Slate light background
        self.CARD_BG = "#ffffff"          # White cards
        self.PRIMARY_COLOR = "#2563eb"     # Royal blue accent
        self.TEXT_MAIN = "#0f172a"        # Deep slate text
        self.TEXT_MUTED = "#64748b"       # Muted gray text
        self.ERROR_COLOR = "#dc2626"      # Danger red
        self.SUCCESS_COLOR = "#16a34a"    # Success green
        self.BORDER_COLOR = "#e2e8f0"     # Light gray border

        self.root.configure(bg=self.BG_COLOR)

        # Build UI layout
        self._setup_styles()
        self._build_header()
        self._build_search_bar()
        self._build_status_bar()
        self._build_content_area()

    def _setup_styles(self):
        """Configures ttk styles for consistent widgets."""
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Custom Search Button Style
        self.style.configure(
            "Search.TButton",
            font=("Segoe UI", 11, "bold"),
            background=self.PRIMARY_COLOR,
            foreground="#ffffff",
            borderwidth=0,
            padding=8
        )
        self.style.map(
            "Search.TButton",
            background=[("active", "#1d4ed8"), ("disabled", "#94a3b8")]
        )

    def _build_header(self):
        """Creates the application title and subtitle header."""
        header_frame = tk.Frame(self.root, bg=self.BG_COLOR)
        header_frame.pack(fill="x", padx=25, pady=(20, 10))

        title_lbl = tk.Label(
            header_frame,
            text="🌦️ Weather Forecast",
            font=("Segoe UI", 22, "bold"),
            bg=self.BG_COLOR,
            fg=self.TEXT_MAIN
        )
        title_lbl.pack(anchor="w")

        subtitle_lbl = tk.Label(
            header_frame,
            text="Get real-time weather and 7-day forecasts powered by Open-Meteo",
            font=("Segoe UI", 10),
            bg=self.BG_COLOR,
            fg=self.TEXT_MUTED
        )
        subtitle_lbl.pack(anchor="w", pady=(2, 0))

    def _build_search_bar(self):
        """Creates the city input field and search button."""
        search_card = tk.Frame(
            self.root,
            bg=self.CARD_BG,
            highlightbackground=self.BORDER_COLOR,
            highlightthickness=1,
            padx=12,
            pady=10
        )
        search_card.pack(fill="x", padx=25, pady=(5, 5))

        # Search Entry Field
        self.city_entry = tk.Entry(
            search_card,
            font=("Segoe UI", 12),
            bg="#f8fafc",
            fg=self.TEXT_MAIN,
            relief="flat",
            highlightthickness=1,
            highlightbackground="#cbd5e1",
            highlightcolor=self.PRIMARY_COLOR,
            insertbackground=self.TEXT_MAIN
        )
        self.city_entry.pack(side="left", fill="x", expand=True, ipady=6, padx=(0, 10))
        self.city_entry.insert(0, "Pune")  # Friendly default city
        self.city_entry.bind("<Return>", lambda event: self.search_weather())

        # Search Button
        self.search_btn = ttk.Button(
            search_card,
            text="Get Weather",
            style="Search.TButton",
            command=self.search_weather,
            cursor="hand2"
        )
        self.search_btn.pack(side="right")

    def _build_status_bar(self):
        """Displays status updates, loading spinners, or validation error messages."""
        self.status_label = tk.Label(
            self.root,
            text="Enter a city name and click 'Get Weather' (or press Enter).",
            font=("Segoe UI", 9, "italic"),
            bg=self.BG_COLOR,
            fg=self.TEXT_MUTED
        )
        self.status_label.pack(fill="x", padx=25, pady=(2, 6))

    def _build_content_area(self):
        """Sets up the scrollable or stacked area for current weather & forecast."""
        self.content_frame = tk.Frame(self.root, bg=self.BG_COLOR)
        self.content_frame.pack(fill="both", expand=True, padx=25, pady=(0, 15))

        # --- Section 1: Current Weather Card ---
        self.current_card = tk.Frame(
            self.content_frame,
            bg=self.CARD_BG,
            highlightbackground=self.BORDER_COLOR,
            highlightthickness=1,
            padx=18,
            pady=16
        )
        self.current_card.pack(fill="x", pady=(0, 10))

        # City Name & Subtitle
        self.location_label = tk.Label(
            self.current_card,
            text="No city selected",
            font=("Segoe UI", 16, "bold"),
            bg=self.CARD_BG,
            fg=self.TEXT_MAIN,
            anchor="w"
        )
        self.location_label.pack(fill="x")

        self.time_label = tk.Label(
            self.current_card,
            text="Search for a city to load data",
            font=("Segoe UI", 9),
            bg=self.CARD_BG,
            fg=self.TEXT_MUTED,
            anchor="w"
        )
        self.time_label.pack(fill="x", pady=(2, 10))

        # Temp + Icon Row
        temp_row = tk.Frame(self.current_card, bg=self.CARD_BG)
        temp_row.pack(fill="x", pady=(0, 12))

        self.temp_label = tk.Label(
            temp_row,
            text="--°C",
            font=("Segoe UI", 36, "bold"),
            bg=self.CARD_BG,
            fg=self.PRIMARY_COLOR
        )
        self.temp_label.pack(side="left")

        self.condition_label = tk.Label(
            temp_row,
            text="--",
            font=("Segoe UI", 14),
            bg=self.CARD_BG,
            fg=self.TEXT_MAIN,
            padx=15
        )
        self.condition_label.pack(side="left")

        # Weather Attributes Grid (Feels Like, Humidity, Wind)
        details_frame = tk.Frame(self.current_card, bg="#f8fafc", padx=12, pady=10)
        details_frame.pack(fill="x")

        # Attribute 1: Feels Like
        self.feels_label = tk.Label(
            details_frame,
            text="Feels like: --°C",
            font=("Segoe UI", 10),
            bg="#f8fafc",
            fg=self.TEXT_MAIN
        )
        self.feels_label.pack(side="left", expand=True)

        # Attribute 2: Humidity
        self.humidity_label = tk.Label(
            details_frame,
            text="💧 Humidity: --%",
            font=("Segoe UI", 10),
            bg="#f8fafc",
            fg=self.TEXT_MAIN
        )
        self.humidity_label.pack(side="left", expand=True)

        # Attribute 3: Wind
        self.wind_label = tk.Label(
            details_frame,
            text="💨 Wind: -- km/h",
            font=("Segoe UI", 10),
            bg="#f8fafc",
            fg=self.TEXT_MAIN
        )
        self.wind_label.pack(side="left", expand=True)

        # --- Section 2: 7-Day Forecast Section ---
        forecast_header_frame = tk.Frame(self.content_frame, bg=self.BG_COLOR)
        forecast_header_frame.pack(fill="x", pady=(5, 6))

        forecast_title = tk.Label(
            forecast_header_frame,
            text="📅 7-Day Forecast",
            font=("Segoe UI", 12, "bold"),
            bg=self.BG_COLOR,
            fg=self.TEXT_MAIN
        )
        forecast_title.pack(anchor="w")

        # Container for the 7 forecast rows
        self.forecast_card = tk.Frame(
            self.content_frame,
            bg=self.CARD_BG,
            highlightbackground=self.BORDER_COLOR,
            highlightthickness=1,
            padx=12,
            pady=8
        )
        self.forecast_card.pack(fill="both", expand=True)

        # Placeholder label before first search
        self.forecast_placeholder = tk.Label(
            self.forecast_card,
            text="7-Day forecast will be displayed here.",
            font=("Segoe UI", 10, "italic"),
            bg=self.CARD_BG,
            fg=self.TEXT_MUTED,
            pady=40
        )
        self.forecast_placeholder.pack()

    # ---------------- Network & Data Handling ----------------

    def search_weather(self):
        """
        Triggered when user clicks Search button or presses Enter.
        Validates the input and spawns a background thread to prevent UI freezing.
        """
        city = self.city_entry.get().strip()
        if not city:
            self._set_status("⚠️ Please enter a city name to search.", self.ERROR_COLOR)
            return

        # Disable button and display loading indicator
        self.search_btn.config(state="disabled")
        self._set_status(f"🔍 Searching weather for '{city}'...", self.PRIMARY_COLOR)

        # Run API call in a daemon thread so GUI stays responsive
        thread = threading.Thread(target=self._fetch_data_worker, args=(city,), daemon=True)
        thread.start()

    def _fetch_data_worker(self, city: str):
        """Worker thread to execute network requests without blocking Tkinter."""
        try:
            # 1. Geocode city name to lat/lon
            location = get_coordinates(city)

            # 2. Fetch current & 7-day forecast
            weather = get_weather_data(location["latitude"], location["longitude"])

            # Schedule UI update on main thread
            self.root.after(0, self._render_success, location, weather)

        except ValueError as ve:
            self.root.after(0, self._render_error, str(ve))
        except ConnectionError as ce:
            self.root.after(0, self._render_error, str(ce))
        except Exception as ex:
            self.root.after(0, self._render_error, f"An unexpected error occurred: {ex}")

    def _render_success(self, location: dict, weather: dict):
        """Updates all GUI elements with the fresh weather data (Main Thread)."""
        current = weather["current"]
        forecast_days = weather["forecast"]

        # Update Current Weather Card
        self.location_label.config(text=location["display_name"])
        self.time_label.config(text=f"Updated: {current['time']} (Timezone: {location['timezone']})")
        self.temp_label.config(text=f"{current['temperature']}°C")
        self.condition_label.config(text=f"{current['icon']}  {current['condition']}")
        self.feels_label.config(text=f"Feels like: {current['feels_like']}°C")
        self.humidity_label.config(text=f"💧 Humidity: {current['humidity']}%")
        self.wind_label.config(text=f"💨 Wind: {current['wind_speed']} km/h")

        # Update 7-Day Forecast Rows
        # Remove placeholder and old rows
        for child in self.forecast_card.winfo_children():
            child.destroy()

        for day in forecast_days:
            row_frame = tk.Frame(self.forecast_card, bg=self.CARD_BG, pady=4)
            row_frame.pack(fill="x", expand=True)

            # Day & Date column
            day_text = f"{day['day_name']} ({day['date']})"
            lbl_day = tk.Label(
                row_frame,
                text=day_text,
                font=("Segoe UI", 10, "bold" if day["day_name"] == "Today" else "normal"),
                bg=self.CARD_BG,
                fg=self.PRIMARY_COLOR if day["day_name"] == "Today" else self.TEXT_MAIN,
                width=16,
                anchor="w"
            )
            lbl_day.pack(side="left")

            # Condition & Icon column
            cond_text = f"{day['icon']} {day['condition']}"
            lbl_cond = tk.Label(
                row_frame,
                text=cond_text,
                font=("Segoe UI", 9),
                bg=self.CARD_BG,
                fg=self.TEXT_MAIN,
                anchor="w"
            )
            lbl_cond.pack(side="left", fill="x", expand=True, padx=5)

            # Rain probability column
            rain_text = f"🌧️ {day['precipitation_prob']}%"
            lbl_rain = tk.Label(
                row_frame,
                text=rain_text,
                font=("Segoe UI", 9),
                bg=self.CARD_BG,
                fg="#0284c7" if day['precipitation_prob'] > 20 else self.TEXT_MUTED,
                width=8,
                anchor="center"
            )
            lbl_rain.pack(side="left", padx=5)

            # Temp Min / Max column
            temp_range = f"{day['temp_min']}°C  /  {day['temp_max']}°C"
            lbl_temp = tk.Label(
                row_frame,
                text=temp_range,
                font=("Segoe UI", 9, "bold"),
                bg=self.CARD_BG,
                fg=self.TEXT_MAIN,
                width=14,
                anchor="e"
            )
            lbl_temp.pack(side="right")

            # Divider line between rows
            divider = tk.Frame(self.forecast_card, bg="#f1f5f9", height=1)
            divider.pack(fill="x", pady=(2, 2))

        # Re-enable search button and set status
        self.search_btn.config(state="normal")
        self._set_status(f"✅ Weather data loaded for {location['name']}.", self.SUCCESS_COLOR)

    def _render_error(self, message: str):
        """Displays error message and resets button state (Main Thread)."""
        self.search_btn.config(state="normal")
        self._set_status(f"❌ {message}", self.ERROR_COLOR)

    def _set_status(self, text: str, color: str):
        """Helper to update status label text and color."""
        self.status_label.config(text=text, fg=color)
