"""
main.py - Weather Forecasting Application Entry Point
------------------------------------------------------
Initializes and launches the Tkinter Weather Forecasting application.

To run:
    python main.py
"""

import sys
import tkinter as tk
from gui import WeatherApp


def main():
    """Initializes the main window and runs the GUI event loop."""
    root = tk.Tk()

    # Optional: configure window behavior
    # Center window on screen
    window_width = 640
    window_height = 780
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int((screen_width / 2) - (window_width / 2))
    center_y = int((screen_height / 2) - (window_height / 2))
    root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

    # Initialize WeatherApp
    app = WeatherApp(root)

    # Automatically fetch initial weather for default city (Pune) on launch
    root.after(200, app.search_weather)

    # Start Tkinter main event loop
    root.mainloop()


if __name__ == "__main__":
    main()
