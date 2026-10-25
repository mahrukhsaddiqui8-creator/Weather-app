import os
import requests
import gradio as gr

# =====================================
# Get API key from Hugging Face Secrets
# =====================================
API_KEY = os.getenv("weatherAPI_key")


def get_weather(city):

    if city.strip() == "":
        return "⚠️ Please enter a city name."

    if not API_KEY:
        return "❌ API key not found. Please add WEATHER_API_KEY in Hugging Face Secrets."

    url = f"https://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}&aqi=yes"

    try:
        response = requests.get(url)
        data = response.json()

        if "error" in data:
            return f"❌ {data['error']['message']}"

        location = data["location"]
        current = data["current"]

        weather_info = f"""
🌍 Location: {location['name']}, {location['region']}, {location['country']}

🕒 Local Time: {location['localtime']}

🌡 Temperature: {current['temp_c']} °C

🤒 Feels Like: {current['feelslike_c']} °C

🌤 Condition: {current['condition']['text']}

💧 Humidity: {current['humidity']} %

🌬 Wind Speed: {current['wind_kph']} km/h

🧭 Wind Direction: {current['wind_dir']}

📊 Pressure: {current['pressure_mb']} mb

☁ Cloud Cover: {current['cloud']} %

👀 Visibility: {current['vis_km']} km

🌞 UV Index: {current['uv']}

🌫 Air Quality Index (US EPA): {current['air_quality']['us-epa-index']}
"""

        return weather_info

    except Exception as e:
        return f"❌ Error: {str(e)}"


demo = gr.Interface(
    fn=get_weather,
    inputs=gr.Textbox(
        label="🌍 City Name",
        placeholder="Enter a city (e.g., Lahore)"
    ),
    outputs=gr.Textbox(
        label="Current Weather",
        lines=18
    ),
    title="🌦 Weather Application",
    description="Enter any city name to view the current weather using WeatherAPI.com."
)

if __name__ == "__main__":
    demo.launch()
