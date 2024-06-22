import pandas as pd
import requests
import os

# OpenWeather API key
open_weather_api_key = os.getenv("OPENWEATHER_API_KEY")

if not open_weather_api_key:
    raise ValueError("OpenWeather API key not found. Please set the OPENWEATHER_API_KEY environment variable.")

# Dictionary of locations with their coordinates
city_locations = {
    "Cumbria": {"latitude": 54.4609, "longitude": -3.0886},
    "Corfe Castle": {"latitude": 50.6395, "longitude": -2.0566},
    "The Cotswolds": {"latitude": 51.8330, "longitude": -1.8433},
    "cambridge": {"latitude": 52.2053, "longitude": 0.1218},
    "Bristol": {"latitude": 51.4545, "longitude": -2.5879},
    "Oxford": {"latitude": 51.7520, "longitude": -1.2577},
    "Norwich": {"latitude": 52.6309, "longitude": 1.2974},
    "Stonehenge": {"latitude": 51.1789, "longitude": -1.8262},
    "Watergate Bay": {"latitude": 50.4429, "longitude": -5.0553},
    "Birmingham": {"latitude": 52.4862, "longitude": -1.8904}
}


# This function gets the daily weather forecast
def get_daily_forecast(lat, lon, open_weather_api_key):
    url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={open_weather_api_key}"
    response = requests.get(url)
    data = response.json()

    daily_forecast = []

    # Processes the JSON response to extract weather data for 12:00PM each day
    if "list" in data:
        for forecast in data["list"]:
            if forecast["dt_txt"].split()[1] == "12:00:00":
                timestamp = forecast["dt_txt"]
                temp_k = forecast["main"]["temp"]
                temp_c = temp_k - 273.15
                description = forecast["weather"][0]["description"]

                daily_forecast.append({
                    "Timestamp": timestamp,
                    "Temperature (Celsius)": f"{temp_c:.2f}",
                    "Description": description
                })

    return daily_forecast


if __name__ == "__main__":
    # Collects forecast data
    # Adds city names to forecast data and collects it all in a list
    all_forecast_data = []

    for city, coordinates in city_locations.items():
        lat = coordinates["latitude"]
        lon = coordinates["longitude"]

        daily_forecast = get_daily_forecast(lat, lon, open_weather_api_key)

        for entry in daily_forecast:
            entry["City"] = city  # Add city name to the entry
            all_forecast_data.append(entry)

    # Creates a DataFrame and saves it to a CSV file
    df = pd.DataFrame(all_forecast_data)

    output_csv = "training_data/all_locations_daily_forecast.csv"

    df.to_csv(output_csv, index=False, encoding='utf-8')

    print(f"All daily forecast data saved to {output_csv}")
