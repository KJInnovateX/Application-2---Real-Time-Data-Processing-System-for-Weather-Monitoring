import unittest
from test.test_api import fetch_weather, fetch_weather_data  # Adjust based on your structure

class TestWeatherAPI(unittest.TestCase):

    def test_fetch_weather_valid_city(self):
        """Test the weather fetching function with a valid city."""
        result = fetch_weather('Delhi')
        self.assertIn('temp', result)
        self.assertNotIn('error', result)

    def test_fetch_weather_invalid_city(self):
        """Test the weather fetching function with an invalid city."""
        result = fetch_weather('InvalidCityName')
        self.assertIn('error', result)

    def test_fetch_weather_missing_key(self):
        """Test when API key is missing."""
        # Simulate missing API key scenario
        result = fetch_weather('Delhi')
        self.assertIn('error', result)
    
    def test_fetch_weather_data_multiple(self):
        """Test fetching data for multiple cities."""
        cities = ['Delhi', 'Mumbai', 'InvalidCity']
        result = fetch_weather_data(cities)
        self.assertEqual(len(result), 3)

if __name__ == '__main__':
    unittest.main()
