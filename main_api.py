from fastapi import FastAPI, Query, Request, Form
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn

# Import all the existing weather functions
from project import get_weather, get_advice, advice_temperature, get_weather_emoji

app = FastAPI(
    title="World Weather Checker API",
    description="Check the weather and get recommendations for any city.",
    version="1.0.0",
)

# Set up templates
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🌦️ World Weather Checker</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
            }
            
            .container {
                background: white;
                padding: 40px;
                border-radius: 20px;
                box-shadow: 0 15px 35px rgba(0,0,0,0.1);
                text-align: center;
                max-width: 500px;
                width: 100%;
            }
            
            h1 {
                color: #2d3436;
                margin-bottom: 10px;
                font-size: 2.5em;
            }
            
            .subtitle {
                color: #636e72;
                margin-bottom: 30px;
                font-size: 1.1em;
            }
            
            .form-group {
                margin-bottom: 25px;
            }
            
            input[type="text"] {
                width: 100%;
                padding: 15px;
                border: 2px solid #ddd;
                border-radius: 10px;
                font-size: 16px;
                transition: border-color 0.3s;
            }
            
            input[type="text"]:focus {
                outline: none;
                border-color: #74b9ff;
            }
            
            button {
                background: linear-gradient(135deg, #00b894 0%, #00a085 100%);
                color: white;
                padding: 15px 30px;
                border: none;
                border-radius: 10px;
                font-size: 16px;
                cursor: pointer;
                transition: transform 0.2s;
                width: 100%;
            }
            
            button:hover {
                transform: translateY(-2px);
            }
            
            .instructions {
                background: #f8f9fa;
                padding: 20px;
                border-radius: 10px;
                margin-top: 30px;
                text-align: left;
            }
            
            .instructions h3 {
                color: #2d3436;
                margin-bottom: 15px;
            }
            
            .instructions ul {
                color: #636e72;
                padding-left: 20px;
            }
            
            .instructions li {
                margin-bottom: 8px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🌦️ World Weather Checker</h1>
            <p class="subtitle">Get current weather and personalized recommendations for any city!</p>
            
            <form action="/weather" method="get">
                <div class="form-group">
                    <input type="text" name="city" placeholder="Enter city name (e.g., Tokyo, New York, London)" required>
                </div>
                <button type="submit">🌍 Check Weather</button>
            </form>
            
            <div class="instructions">
                <h3>How to use:</h3>
                <ul>
                    <li>Enter any city name in the world</li>
                    <li>Get current temperature and weather conditions</li>
                    <li>Receive personalized recommendations based on weather</li>
                    <li>See weather emojis to make it more visual! 🌤️</li>
                </ul>
            </div>
        </div>
    </body>
    </html>
    """


@app.get("/weather", response_class=HTMLResponse)
def get_weather_route(city: str = Query(..., description="Name of the city")):
    # Use the existing weather checking logic correctly
    weather_result = get_weather(city.strip())

    if weather_result == "Error":
        return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>🌦️ Weather Error</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: linear-gradient(135deg, #ff7675 0%, #d63031 100%);
                    min-height: 100vh;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    padding: 20px;
                }}
                .container {{
                    background: white;
                    padding: 40px;
                    border-radius: 20px;
                    box-shadow: 0 15px 35px rgba(0,0,0,0.1);
                    text-align: center;
                    max-width: 500px;
                }}
                .error {{
                    color: #d63031;
                    font-size: 1.5em;
                    margin-bottom: 20px;
                }}
                .back-btn {{
                    background: #0984e3;
                    color: white;
                    padding: 10px 20px;
                    text-decoration: none;
                    border-radius: 10px;
                    display: inline-block;
                    margin-top: 20px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>⚠️</h1>
                <p class="error">Error fetching weather data for "{city}"</p>
                <p>Please double check the name of the city and try again.</p>
                <a href="/" class="back-btn">← Try Again</a>
            </div>
        </body>
        </html>
        """

    # Extract temperature and description from the returned list
    temp, desc = weather_result

    # Get advice and emojis using existing functions
    advice = get_advice(desc)
    advice_temp = advice_temperature(temp)
    weather_emoji = get_weather_emoji(desc)

    # Combine temperature advice with weather advice
    full_advice = f"{advice_temp} {advice}".strip()

    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🌦️ Weather in {city.title()}</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #00b894 0%, #00a085 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
            }}
            .container {{
                background: white;
                padding: 40px;
                border-radius: 20px;
                box-shadow: 0 15px 35px rgba(0,0,0,0.1);
                text-align: center;
                max-width: 600px;
                width: 100%;
            }}
            .city-name {{
                color: #2d3436;
                font-size: 2.5em;
                margin-bottom: 10px;
            }}
            .weather-emoji {{
                font-size: 4em;
                margin: 20px 0;
            }}
            .temperature {{
                font-size: 3em;
                color: #0984e3;
                font-weight: bold;
                margin: 20px 0;
            }}
            .description {{
                font-size: 1.5em;
                color: #636e72;
                margin-bottom: 30px;
                text-transform: capitalize;
            }}
            .advice {{
                background: #f8f9fa;
                padding: 25px;
                border-radius: 15px;
                margin: 30px 0;
                border-left: 5px solid #00b894;
            }}
            .advice-title {{
                color: #2d3436;
                font-size: 1.3em;
                font-weight: bold;
                margin-bottom: 10px;
            }}
            .advice-text {{
                color: #636e72;
                font-size: 1.1em;
                line-height: 1.6;
            }}
            .back-btn {{
                background: #0984e3;
                color: white;
                padding: 15px 30px;
                text-decoration: none;
                border-radius: 10px;
                display: inline-block;
                margin-top: 20px;
                transition: transform 0.2s;
            }}
            .back-btn:hover {{
                transform: translateY(-2px);
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1 class="city-name">{city.title()}</h1>
            
            <div class="weather-emoji">{weather_emoji}</div>
            
            <div class="temperature">{temp}°C</div>
            
            <p class="description">{desc}</p>
            
            <div class="advice">
                <div class="advice-title">💡 Recommendations</div>
                <div class="advice-text">{full_advice}</div>
            </div>
            
            <a href="/" class="back-btn">🔄 Check Another City</a>
        </div>
    </body>
    </html>
    """


if __name__ == "__main__":
    uvicorn.run("main_api:app", host="0.0.0.0", port=8000, reload=True)
