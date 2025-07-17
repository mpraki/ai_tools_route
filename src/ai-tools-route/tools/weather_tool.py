from logging import info

import requests
from langchain_core.tools import tool
from pydantic import BaseModel, Field


class OpenMeteoInput(BaseModel):
    """Fetch the current temperature in °C for given coordinates."""

    latitude: float = Field(..., title="Latitude", description="Latitude of the location to fetch weather for.")
    longitude: float = Field(..., title="Longitude", description="Longitude of the location to fetch weather for.")


@tool(args_schema=OpenMeteoInput)
def get_current_temperature(latitude: float, longitude: float) -> str:
    """Fetch current temperature in degree Celcius for given coordinates."""

    info(f"Fetching current temperature for coordinates: ({latitude}, {longitude})")

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'hourly': 'temperature_2m',
        'forecast_days': 1,
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        return "Error fetching data from Open-Meteo API."

    # Parse the JSON response
    data = response.json()

    info(f"Fetched data: {data}")

    # {'latitude': 11.5, 'longitude': 78.75, 'generationtime_ms': 0.03039836883544922, 'utc_offset_seconds': 0, 'timezone': 'GMT', 'timezone_abbreviation': 'GMT', 'elevation': 224.0, 'hourly_units': {'time': 'iso8601', 'temperature_2m': '°C'}, 'hourly': {'time': ['2025-07-17T00:00', '2025-07-17T01:00', '2025-07-17T02:00', '2025-07-17T03:00', '2025-07-17T04:00', '2025-07-17T05:00', '2025-07-17T06:00', '2025-07-17T07:00', '2025-07-17T08:00', '2025-07-17T09:00', '2025-07-17T10:00', '2025-07-17T11:00', '2025-07-17T12:00', '2025-07-17T13:00', '2025-07-17T14:00', '2025-07-17T15:00', '2025-07-17T16:00', '2025-07-17T17:00', '2025-07-17T18:00', '2025-07-17T19:00', '2025-07-17T20:00', '2025-07-17T21:00', '2025-07-17T22:00', '2025-07-17T23:00'], 'temperature_2m': [25.0, 25.0, 26.1, 27.7, 29.5, 31.4, 32.9, 34.0, 34.1, 34.4, 34.6, 33.3, 33.0, 31.2, 30.0, 29.1, 28.3, 27.8, 27.3, 26.7, 26.3, 26.0, 25.9, 25.7]}}
    if 'hourly' not in data or 'temperature_2m' not in data['hourly']:
        return "No temperature data available for the specified coordinates."
    temperatures = data['hourly']['temperature_2m']
    if not temperatures:
        return "No temperature data available for the specified coordinates."
    current_temperature = temperatures[0]
    max_temperature = max(temperatures)
    min_temperature = min(temperatures)

    return f"The current temperature at ({latitude}, {longitude}) is {current_temperature} degree celcius. Max temperature is {max_temperature} and min temperature is {min_temperature}."
