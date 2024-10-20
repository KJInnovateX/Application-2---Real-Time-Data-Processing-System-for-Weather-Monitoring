from flask import Flask, render_template, jsonify, request
from datetime import datetime, timezone
import sys
import os
import plotly
import plotly.graph_objs as go
import json
from dotenv import load_dotenv
load_dotenv()

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.weather_data import fetch_weather_data

app = Flask(__name__)

# Global variable to store user-defined alerts
user_alerts = {}

# Define a filter to convert a timestamp to a readable datetime
def timestamp_to_datetime(timestamp):
    return datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S')

# Register the custom filter
app.jinja_env.filters['timestamp_to_datetime'] = timestamp_to_datetime

def generate_plot(weather_data):
    cities = list(weather_data.keys())
    temperatures = [data['temp'] for data in weather_data.values()]
    timestamps = [timestamp_to_datetime(data['dt']) for data in weather_data.values()]

    fig = go.Figure()

    # Create a line plot for temperature
    fig.add_trace(go.Scatter(x=timestamps, y=temperatures, mode='lines+markers', name='Temperature'))

    fig.update_layout(title='Temperature Trend for Selected Cities', xaxis_title='Timestamp', yaxis_title='Temperature (°C)')
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

@app.route('/')
def index():
    # Fetch initial weather data for the main page
    cities = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']
    weather_data = fetch_weather_data(cities)
    
    # Pass the fetched weather data and user alerts to the index.html
    return render_template('index.html', data=weather_data, alerts=user_alerts)

@app.route('/weather-data', methods=['GET'])
def get_weather_data():
    cities = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']
    weather_data = fetch_weather_data(cities)

    # Generate the plot for the current weather data
    plot_data = generate_plot(weather_data)

    # Check if any alerts should be triggered
    alerts_triggered = []
    for city, info in weather_data.items():
        if city in user_alerts and info['temp'] >= user_alerts[city]:
            alerts_triggered.append(f"Alert for {city}: Temperature ({info['temp']}°C) exceeds the threshold ({user_alerts[city]}°C)")

    # Return the weather data, plot data, and any triggered alerts as JSON
    return jsonify({
        'weather_data': weather_data,
        'plot_data': plot_data,
        'alerts_triggered': alerts_triggered
    })

@app.route('/set-alert', methods=['POST'])
def set_alert():
    data = request.json
    city = data['city']
    threshold = data['threshold']

    # Save the user alert in the global dictionary
    user_alerts[city] = threshold

    return jsonify({'message': f'Alert set for {city} at {threshold}°C'}), 200

if __name__ == '__main__':
    app.run(debug=True)
