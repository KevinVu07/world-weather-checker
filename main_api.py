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
def get_weather_route(
    city: str = Query(..., description="City name to check weather for")
):
    try:
        result = get_weather(city)
        if result == "Error":
            return JSONResponse(
                content={"error": "City not found or API issue"}, status_code=404
            )
        temp, desc = result
        return {"city": city, "temperature_celsius": temp, "description": desc}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


if __name__ == "__main__":
    uvicorn.run("main_api:app", host="0.0.0.0", port=8000, reload=True)
