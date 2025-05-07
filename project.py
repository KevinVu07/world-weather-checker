import requests
import math
import sys
import argparse


def main():
    parser = argparse.ArgumentParser(
        description="Get the current weather of any city in the world"
    )
    parser.add_argument(
        "-c",
        nargs="*",
        help="Name of the city that you want to get the current weather info for",
    )
    args = parser.parse_args()
    if len(sys.argv) > 2:
        city = " ".join(args.c)
    elif len(sys.argv) == 2:
        city = args.c
    else:
        city = input("Which city would you like to get current weather info for: ")

    if get_weather(city) == "Error":
        sys.exit(
            "Error fetching weather data. Please double check the name of the city."
        )
    else:
        temp, desc = get_weather(city)
        advice = get_advice(desc)
        advice_temp = advice_temperature(temp)
        weather_emoji = get_weather_emoji(desc)

        print(
            f"The weather is {desc} {weather_emoji} today, temperature is {temp}\xb0C. {advice_temp} {advice}"
        )


def get_weather(city):
    api_key = "bfaed45a59121dcc1a3aaaa7c2ceaf64"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    try:
        response = requests.get(url)
        data = response.json()
        # print(data)
        temp = math.ceil(data["main"]["temp"] - 273.15)
        desc = data["weather"][0]["description"]
        return [temp, desc]
    except Exception:
        return "Error"


def get_weather_emoji(weather):
    if "rain" in weather:
        return "🌧️"
    elif "cloud" in weather:
        return "🌥️"
    elif "storm" in weather:
        return "⛈️"
    elif "sunny" in weather:
        return "☀️"
    elif "snow" in weather:
        return "⛄️"
    else:
        return ""


def get_advice(weather):
    if "rain" in weather:
        return "Bring an umbrella!"
    elif "sun" in weather:
        return "Wear sunscreen, and bring a hat!"
    elif "storm" in weather:
        return "It is better to stay inside!"
    else:
        return "Have a good day!"


def advice_temperature(temp):
    if temp <= 5:
        return "Oh it is frosty, bring a thick coat!"
    elif temp <= 10:
        return "Bring a jacket!"
    elif temp >= 30:
        return "It is a hot day. Stay hydrated!"
    else:
        return ""


if __name__ == "__main__":
    main()
