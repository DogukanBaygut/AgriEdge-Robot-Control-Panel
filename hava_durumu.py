# -*- coding: utf-8 -*-
##
# ==============================================================================
# @file hava_durumu.py
# @brief AGRIEDGE Smart Agriculture Interface – Weather Forecast Module
# @version 2.0
# @date May 4, 2025
# @author Doğukan Avcı
#
# ==============================================================================
# DESCRIPTION:
# ------------------------------------------------------------------------------
# This module is a core part of the AGRIEDGE intelligent farming system. It is
# responsible for fetching and displaying real-time weather forecasts using the
# Open-Meteo API, focusing specifically on the Eskişehir region. The goal is to
# help farmers make informed decisions about watering, hoeing, planting, and
# field maintenance based on upcoming climate conditions.
#
# With this class-based structure (`WeatherFetcher`), the code becomes:
#   - Modular and reusable across different UI components,
#   - Testable and maintainable with encapsulated logic,
#   - Easy to integrate into PyQt5-based applications.
#
# ------------------------------------------------------------------------------
# KEY FEATURES:
# ------------------------------------------------------------------------------
# ✅ Retrieves 7-day weather forecast data from Open-Meteo API
# ✅ Parses and displays:
#     - Daily maximum and minimum temperatures
#     - Daily precipitation (rainfall) values
# ✅ Uses simple rule-based heuristics to classify weather conditions
#     - ☀️ Sunny (0 mm rain)
#     - 🌤️ Partly Cloudy (< 5 mm)
#     - 🌧️ Rain (< 20 mm)
#     - ⛈️ Storm (≥ 20 mm)
# ✅ Renders data in a structured, styled HTML table inside a QTextBrowser
# ✅ Provides fallback warnings if API communication fails
#
# ------------------------------------------------------------------------------
# OBJECT-ORIENTED DESIGN:
# ------------------------------------------------------------------------------
# - @class WeatherFetcher
#   - @encapsulation: Internal data retrieval and rendering logic is self-contained.
#   - @reusability: Supports reuse across multiple GUI views without code duplication.
#   - @integration: Directly renders formatted HTML into a given QTextBrowser widget.
#
# ------------------------------------------------------------------------------
# EXTERNAL DEPENDENCIES:
# ------------------------------------------------------------------------------
# - `requests`   : Handles HTTP GET requests to Open-Meteo API
# - `datetime`   : Used for formatting and parsing date strings
#
# ------------------------------------------------------------------------------
# USAGE EXAMPLE:
# ------------------------------------------------------------------------------
# from hava_durumu import WeatherFetcher
# WeatherFetcher(self.ui.textBrowser_Hava_durumu).render()
#
# This call will fetch and display the weather forecast directly in the QTextBrowser widget.
# ==============================================================================


import requests
from datetime import datetime

class WeatherFetcher:
    """
    Class to fetch and display 7-day weather forecast for Eskişehir using the Open-Meteo API.
    
    Methods:
        - fetch_data(): Retrieves weather JSON from the API.
        - format_html(): Converts raw data into an HTML table.
        - render(): Combines fetching and formatting, then renders HTML to a QTextBrowser.
    """
    
    def __init__(self, text_browser):
        """
        Initializes the WeatherFetcher with a QTextBrowser reference.
        
        Args:
            text_browser (QTextBrowser): The widget where the forecast will be displayed.
        """
        self.text_browser = text_browser
        self.api_url = (
            "https://api.open-meteo.com/v1/forecast?"
            "latitude=39.7767&longitude=30.5206"
            "&daily=temperature_2m_max,temperature_2m_min,precipitation_sum"
            "&timezone=Europe%2FIstanbul"
        )

    def fetch_data(self):
        """
        Fetches weather forecast data from the Open-Meteo API.

        Returns:
            tuple: (dates, max_temps, min_temps, precipitation) if successful.
            None: if the request fails.
        """
        try:
            response = requests.get(self.api_url)
            data = response.json()
            return (
                data['daily']['time'],
                data['daily']['temperature_2m_max'],
                data['daily']['temperature_2m_min'],
                data['daily']['precipitation_sum']
            )
        except Exception as e:
            self.text_browser.setText(f"<b style='color:red;'>⚠️ Failed to retrieve data:</b> {e}")
            return None

    def format_html(self, dates, temps_max, temps_min, precipitation):
        """
        Generates an HTML table representing the forecast.

        Args:
            dates (list): List of forecast dates.
            temps_max (list): Max temperatures.
            temps_min (list): Min temperatures.
            precipitation (list): Precipitation amounts.

        Returns:
            str: Formatted HTML string.
        """
        html = """
        <html><head>
        <style>
            table { width: 100%; border-collapse: collapse; font-family: Arial; font-size: 10pt; }
            th, td { border: 1px solid #ccc; text-align: center; padding: 6px; }
            th { background-color: #f0f0f0; font-weight: bold; }
        </style>
        </head><body>
        <b>📍 Eskişehir 7-Day Weather Forecast</b>
        <table>
            <tr><th>Date</th><th>Condition</th><th>Day</th><th>Night</th><th>Precipitation</th></tr>
        """

        for i in range(len(dates)):
            tarih = datetime.strptime(dates[i], "%Y-%m-%d").strftime("%d %b %a")
            max_temp = round(temps_max[i])
            min_temp = round(temps_min[i])
            rain = precipitation[i]

            if rain == 0:
                icon = "☀️ Sunny"
            elif rain < 5:
                icon = "🌤️ Partly Cloudy"
            elif rain < 20:
                icon = "🌧️ Rain"
            else:
                icon = "⛈️ Storm"

            html += f"""
                <tr>
                    <td>{tarih}</td>
                    <td>{icon}</td>
                    <td>{max_temp}°C</td>
                    <td>{min_temp}°C</td>
                    <td>{rain:.1f} mm</td>
                </tr>
            """

        html += "</table></body></html>"
        return html

    def render(self):
        """
        Fetches weather data and renders the HTML output to the QTextBrowser.
        """
        data = self.fetch_data()
        if data:
            html = self.format_html(*data)
            self.text_browser.setHtml(html)
