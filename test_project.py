import sys
import unittest
from unittest.mock import MagicMock, patch

import requests

from project import get_advice, advice_temperature, get_weather_emoji, get_weather


class TestWeather(unittest.TestCase):
    @patch("project.requests")
    def test_get_weather(self, mock_requests):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "coord": {"lon": 105.8412, "lat": 21.0245},
            "weather": [
                {
                    "id": 804,
                    "main": "Clouds",
                    "description": "overcast clouds",
                    "icon": "04d",
                }
            ],
            "base": "stations",
            "main": {
                "temp": 296.15,
                "feels_like": 295.92,
                "temp_min": 296.15,
                "temp_max": 296.15,
                "pressure": 1026,
                "humidity": 54,
                "sea_level": 1026,
                "grnd_level": 1025,
            },
            "visibility": 10000,
            "wind": {"speed": 5.13, "deg": 354, "gust": 10.5},
            "clouds": {"all": 100},
            "dt": 1700124495,
            "sys": {
                "type": 1,
                "id": 9308,
                "country": "VN",
                "sunrise": 1700089639,
                "sunset": 1700129729,
            },
            "timezone": 25200,
            "id": 1581130,
            "name": "Hanoi",
            "cod": 200,
        }

        mock_requests.get.return_value = mock_response

        self.assertEqual(get_weather("hanoi"), [23, "overcast clouds"])

    @patch("project.requests")
    def test_get_weather_exception(self, mock_requests):
        mock_requests.exceptions = requests.exceptions

        mock_requests.get.side_effect = Exception(
            "Error fetching weather data. Please double check the name of the city."
        )

        self.assertEqual(get_weather("hanol"), "Error")

    def test_get_advice(self):
        self.assertEqual(get_advice("rainy"), "Bring an umbrella!")
        self.assertEqual(get_advice("sunny"), "Wear sunscreen, and bring a hat!")
        self.assertEqual(get_advice("stormy"), "It is better to stay inside!")
        self.assertEqual(get_advice("clear sky"), "Have a good day!")

    def test_advice_temperature(self):
        self.assertEqual(advice_temperature(10), "Bring a jacket!")
        self.assertEqual(advice_temperature(6), "Bring a jacket!")
        self.assertEqual(advice_temperature(5), "Oh it is frosty, bring a thick coat!")
        self.assertEqual(advice_temperature(0), "Oh it is frosty, bring a thick coat!")
        self.assertEqual(advice_temperature(-5), "Oh it is frosty, bring a thick coat!")
        self.assertEqual(advice_temperature(30), "It is a hot day. Stay hydrated!")
        self.assertEqual(advice_temperature(35), "It is a hot day. Stay hydrated!")
        self.assertEqual(advice_temperature(20), "")

    def test_get_weather_emoji(self):
        self.assertEqual(get_weather_emoji("The weather is rainy"), "🌧️")
        self.assertEqual(get_weather_emoji("The weather is broken cloud"), "🌥️")
        self.assertEqual(get_weather_emoji("The weather is storm"), "⛈️")
        self.assertEqual(get_weather_emoji("The weather is sunny"), "☀️")
        self.assertEqual(get_weather_emoji("The weather is snow"), "⛄️")
        self.assertEqual(get_weather_emoji("The weather is clear sky"), "")


if __name__ == "__main__":
    unittest.main()
