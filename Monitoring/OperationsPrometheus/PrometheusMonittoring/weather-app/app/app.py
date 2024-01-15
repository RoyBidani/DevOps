import Api
from flask import Flask, render_template, request
from prometheus_client import start_http_server, Summary, Counter, generate_latest
import logging



# Create a Flask app
app = Flask(__name__)

# Create a Prometheus summary metric for request processing time
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')

# Create a Prometheus counter metric for counting /weather requests
WEATHER_REQUESTS = Counter('weather_requests_total', 'Total number of /weather requests')

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

    # Increment the weather request counter
    WEATHER_REQUESTS.inc()

    return render_template('weather.html', location=location, weather_info=weather_info)

# Add a /metrics route for Prometheus to scrape
@app.route('/metrics')
def metrics():
    return generate_latest()

    
# Configure the logger
logging.basicConfig(filename='app.log', level=logging.DEBUG)

@app.route('/logs')  # Define a route for '/logs'
def index():
    # Log messages with different severity levels
    logging.debug('This is a debug message')  # Log a debug message
    logging.info('This is an info message')    # Log an info message
    logging.warning('This is a warning message')  # Log a warning message
    logging.error('This is an error message')    # Log an error message
    logging.critical('This is a critical message')  # Log a critical message
    return 'Weather App'  # Return 'Weather App' as the response



if __name__ == '__main__':
    # Start the Prometheus HTTP server on port 8000
    start_http_server(8000)
    
    # Start your Flask app on host '0.0.0.0' and port 8080
    app.run(host='0.0.0.0', port=8080)
    

