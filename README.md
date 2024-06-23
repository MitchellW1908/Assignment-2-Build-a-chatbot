# Assignment 2: Build a chatbot

This Python chatbot returns weather information and forecasts for select locations in England. It can also display a map of the chosen location using Google Maps.

# Files

There are two Python files: data_extraction.py and main.py.

data_extraction.py stores the list of locations and their coordinates as a dictionary. It also has functions to retrieve forecast information for each location using OpenWeather API. The data is then converted into a DataFrame and saved as the file "all_locations_daily_forecast.csv".

main.py houses the main Flask app that renders the chatbot in the browser. It also imports the location dictionary from data_extraction.py in order to produce a map using a Google Maps API.

The folder "training_data" houses the forecast csv file and a file called "weather_data.txt", which trains the chatbot.

Finally, the templates folder houses index.html, and the folders static/styles house a css file.

# Instructions

The chatbot can return weather information for the current day, as well as the forecast for the next five days. The chatbot can also provide a map of the chosen area using Google Maps.

The list of locations are as follows:

Cumbria, Corfe Castle, The Cotswolds, Cambridge, Bristol, Oxford, Norwich, Stonehenge, Watergate Bay, Birmingham

To retrieve weather information and maps, use the following phrases:

"What is the weather in (location)"

"What is the forecast for (location)"

"Show me a map of (location)"

A txt file will be submitted containing the API keys for OpenWeather and Google Maps.

In order to run main.py, modify line 70 by removing os.getenv() and replace it with the API key. It should read as follows:

google_maps_api_key = "GOOGLEMAPS API KEY"

In order to run data_extraction.py, modify line 6 by removing os.getenv() and replace it with the API key. It should read as follows:

open_weather_api_key = "OPENWEATHER API KEY"