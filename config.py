import os

class Config:
    API_KEY = os.getenv('API_KEY', 'default')
INTERVAL = 300  # Time interval in seconds for data refresh
TEMP_THRESHOLD = 35  # Temperature threshold for alerts
