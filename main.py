from flask import Flask, request, render_template
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer
from data_extraction import city_locations
import os

# Initialises Flask app
app = Flask(__name__)

# Creates the ChatBot
try:
    my_bot = ChatBot(
        name="PyBot",
        read_only=True,
        logic_adapters=["chatterbot.logic.MathematicalEvaluation", "chatterbot.logic.BestMatch"]
    )
except Exception as e:
    print(f"Error initializing ChatBot: {e}")
    raise


# Loads weather data from a file
def load_weather_data(file_path):
    weather_data = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                question, answer = line.strip().split('|')
                weather_data.append((question, answer))
    except FileNotFoundError:
        print(f"Weather data file not found: {file_path}")
    except Exception as e:
        print(f"Error reading weather data: {e}")
    return weather_data


# Trains the ChatBot with weather data from txt file
weather_data = load_weather_data('training_data/weather_data.txt')

list_trainer = ListTrainer(my_bot)
for question, answer in weather_data:
    try:
        list_trainer.train([question, answer])
    except Exception as e:
        print(f"Error training with weather data: {e}")

# Trains ChatBot with ChatterBotCorpus
corpus_trainer = ChatterBotCorpusTrainer(my_bot)
try:
    corpus_trainer.train('chatterbot.corpus.english')
except Exception as e:
    print(f"Error training with ChatterBot corpus: {e}")


# Generates Google Maps URL based on location
def generate_google_maps_url(location):
    city_name = location
    city_name_lower = city_name.lower()
    city_locations_lower = {k.lower(): v for k, v in city_locations.items()}

    if city_name_lower not in city_locations_lower:
        print(f"City '{city_name}' not found in city_locations")
        return None

    city_coordinates = city_locations_lower[city_name_lower]

    lat = city_coordinates["latitude"]
    lon = city_coordinates["longitude"]

    google_maps_api_key = os.getenv("GOOGLEMAPS_API_KEY")

    if not google_maps_api_key:
        print("Google Maps API key is missing")
        return None

    google_maps_url = f"https://www.google.com/maps/embed/v1/view?key={google_maps_api_key}&center={lat},{lon}&zoom=12"

    # Debugging statement to check the generated URL
    print(f"Generated Google Maps URL: {google_maps_url}")

    if not google_maps_api_key:
        print("Google Maps API key is missing")
        return None
    return google_maps_url


# Main route for Flask app - error handling is included
@app.route('/', methods=['GET', 'POST'])
def index():
    chat_history = []
    map_url = None
    if request.method == 'POST':
        user_input = request.form['user_input']
        chat_history = request.form.getlist('chat_history')
        chat_history.append(f'You: {user_input}')

        try:
            bot_response = my_bot.get_response(user_input)
        except Exception as e:
            print(f"Error getting bot response: {e}")
            bot_response = "Sorry, something went wrong."

        chat_history.append(f'Bot: {bot_response}')

        if "show me a map of" in user_input.lower():
            location = user_input.lower().replace("show me a map of", "").strip()
            map_url = generate_google_maps_url(location)
            if map_url:
                chat_history.append('Bot: Sure!')
            else:
                chat_history.append("Bot: Sorry, I can't show the map right now.")

    return render_template('index.html', chat_history=chat_history, map_url=map_url)


if __name__ == "__main__":
    try:
        app.run(debug=True)
    except Exception as e:
        print(f"Error running Flask app: {e}")
