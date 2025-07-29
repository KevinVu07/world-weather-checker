from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import uvicorn
from fastapi.responses import HTMLResponse

from project import get_weather

app = FastAPI(
    title="World Weather Checker API",
    description="Check the weather and get recommendations for any city.",
    version="1.0.0",
)


@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <html>
      <head>
        <title>World Weather Checker</title>
      </head>
      <body>
        <h1>🌦️ Welcome to World Weather Checker!</h1>
        <p>Use the <code>/weather?city=tokyo</code> endpoint to check the weather.</p>
      </body>
    </html>
    """


@app.get("/weather")
def get_weather_route(city: str = "Sydney"):
    result = get_weather(city)  # call your core logic
    if "error" in result:
        return f"<h3>⚠️ {result['error']}</h3>"

    return f"""
    <html>
        <body>
            <h2>🌤️ Weather in {result['city']}</h2>
            <p>Temperature: {result['temperature']}°C</p>
            <p>Conditions: {result['weather']}</p>
            <p>📝 Recommendation: {result['recommendation']}</p>
        </body>
    </html>
    """


if __name__ == "__main__":
    uvicorn.run("main_api:app", host="0.0.0.0", port=8000, reload=True)
