import Api
from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/weather", methods=['POST'])
def weather_display():
    location = request.form['location']
    weather_info = Api.get_weather(location)

    if weather_info[0]['cod'] == '404':
        error_message = 'City not found. Please enter a valid city.'
        return render_template('index.html', error_message=error_message)

    return render_template('weather.html', location=location, weather_info=weather_info)


if __name__ == '__main__':
    app.run()
