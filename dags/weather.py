import os
import csv
from pathlib import Path
import requests

def fetch_weather() -> dict:
    """
    Fetch current weather data for Moscow from OpenWeatherMap API.

    Returns:
        dict: JSON response as a Python dictionary.
    """
    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        raise ValueError("WEATHER_API_KEY is not set in the environment.")
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": "Moscow", "appid": api_key, "units": "metric"}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

def write_weather_to_csv() -> None:
    """
    Fetch weather data and append it as a new row to dataset/weather.csv.

    If the file does not exist, writes a header row first.
    """
    data = fetch_weather()
    dt = data.get("dt")
    city = data.get("name")
    weather_info = data.get("weather", [{}])[0]
    main = data.get("main", {})
    wind = data.get("wind", {})

    row = [
        dt,
        city,
        weather_info.get("main"),
        weather_info.get("description"),
        main.get("temp"),
        main.get("feels_like"),
        main.get("pressure"),
        wind.get("speed"),
    ]
    header = [
        "datetime",
        "city",
        "weather_main",
        "weather_description",
        "temp",
        "feels_like",
        "pressure",
        "wind_speed",
    ]
    dataset_dir = Path(__file__).parent / "dataset"
    dataset_dir.mkdir(parents=True, exist_ok=True)
    csv_file = dataset_dir / "weather.csv"
    write_header = not csv_file.exists()
    with open(csv_file, mode="a", newline="") as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(header)
        writer.writerow(row) 