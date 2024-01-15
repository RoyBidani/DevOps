import Api
from flask import Flask, render_template, request, send_file, jsonify, make_response
import requests
import io
import os
import json
from datetime import datetime

app = Flask(__name__)

# Default background color (if ENV variable is not set)
BG_COLOR = '#f2f2f2'
# Get the background color from the ENV variable, use the default if not set
app.config['BG_COLOR'] = os.environ.get('BG_COLOR', BG_COLOR)


def save_search_history(date, city):
    history_data = []
    filename = 'search_history.json'

    # Check if the history file exists
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            history_data = json.load(file)

    # Append the new search query to the history
    history_data.append({'date': date, 'city': city})

    # Save the updated history to the file
    with open(filename, 'w') as file:
        json.dump(history_data, file)
        file.write('\n')



@app.route('/')
def home():
    return render_template('index.html', BG_COLOR=app.config['BG_COLOR'])


@app.route("/weather", methods=['POST'])
def weather_display():
    location = request.form['location']
    weather_info = Api.get_weather(location)

    if weather_info[0]['cod'] == '404':
        error_message = 'City not found. Please enter a valid city.'
        return render_template('index.html', error_message=error_message)

    # Save the search query to the history
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    save_search_history(date, location)

    return render_template('weather.html', location=location, weather_info=weather_info, BG_COLOR=app.config['BG_COLOR'])


@app.route("/history")
def search_history():
    with open('search_history.json', 'r') as file:
        search_history = json.load(file)
    return render_template('history.html', search_history=search_history)

@app.route("/download/<city>")
def download_history(city):
    with open('search_history.json', 'r') as file:
        search_history = json.load(file)

    # Create a list of search entries for the specified city
    city_searches = [entry for entry in search_history if entry['city'] == city]

    # Create a downloadable JSON file
    response = make_response(json.dumps(city_searches, indent=4))
    response.headers['Content-Disposition'] = f'attachment; filename={city}_search_history.json'
    response.headers['Content-Type'] = 'application/json'
    return response




if __name__ == '__main__':
    print("BG_COLOR:", app.config['BG_COLOR'])  # Print BG_COLOR value before starting the app
    app.run()


