# YOUR PROJECT TITLE

World Weather Checker

#### Video Demo:

<URL https://youtu.be/4eMARw4fMhQ>

#### Description:

    This program allows you to check the current weather of any city in the world. To do that, you simply need to enter the name of the city as the input to the program, and it will output the current weather of that city, coupled with some recommendations based on the weather.

    You can also input the name of the city at the same time while running the program by input it as one of the command line arguments. The format is:

    python project.py -c <CITY NAME>

    The command line arguments input was created with argparse with nargs="*" to allow multiple string arguments in case the city name has more than 1 string. The city name is then "collected" by joining the strings together to one city name.

    For help about the information of the project, enter python project.py -h. The help will show what the program does and how to use it with command line arguments.

    TESTING:

    This program is tested by utilising Python's unittest library. The function get_weather that has an API call to the OpenWeather API was tested by the MagicMock class inside the unittest library, "faking" a JSON object as a result from the API call to test the function.

    The exception case in the API call is also tested by the mock library. The mock raises a side effect of an exception when pass in a typo city name.

    The remaining functions (get_advice, advice_temperature, get_weather_emoji) are tested with manual string input that
    simulate the weather description returned from the real API call.
# world-weather-checker
