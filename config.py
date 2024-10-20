import os

class Config:
    API_KEY = os.getenv('API_KEY', '32cf0eb879d4027cd7ff4649de062975')
INTERVAL = 300  # Time interval in seconds for data refresh
TEMP_THRESHOLD = 35  # Temperature threshold for alerts
