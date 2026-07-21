import requests
from config import OPENWEATHER_API_KEY, OPENWEATHER_BASE_URL, OPENWEATHER_UNITS



def get_weather(city_name,lat=None,lon=None):
    params={
        "appid":OPENWEATHER_API_KEY,
        "units":OPENWEATHER_UNITS,
    }


    if lat is not None and lon is not None:
        params["lat"]=lat
        params["lon"]=lon
    else:
        params["q"]=f"{city_name},IN"

    try:
        response = requests.get(OPENWEATHER_BASE_URL, params=params, timeout=6)
        data = response.json()

        if response.status_code != 200:
            return _empty_weather(error=data.get("message", "Weather data unavailable"))

        weather_main = data.get("weather", [{}])[0].get("main", "Clear")
        weather_desc = data.get("weather", [{}])[0].get("description", "clear sky")
        icon = data.get("weather", [{}])[0].get("icon", "01d")

        rain_prob = 0
        if "rain" in data:
            rain_prob = data["rain"].get("1h", 0) * 100  # rough estimate

        is_rainy = weather_main.lower() in ["rain", "drizzle", "thunderstorm"]

        return {
            "available": True,
            "city": data.get("name", city_name),
            "temperature": round(data.get("main", {}).get("temp", 0), 1),
            "feels_like": round(data.get("main", {}).get("feels_like", 0), 1),
            "humidity": data.get("main", {}).get("humidity", 0),
            "wind_speed": data.get("wind", {}).get("speed", 0),
            "condition": weather_main,
            "description": weather_desc.title(),
            "icon": icon,
            "icon_url": f"https://openweathermap.org/img/wn/{icon}@2x.png",
            "rain_probability": round(rain_prob, 1),
            "is_rainy": is_rainy,
            "recommendation_type": "Indoor" if is_rainy else "Outdoor",
        }

    except (requests.RequestException, ValueError, KeyError):
        return _empty_weather(error="Unable to reach weather service")




# for creating empty weather data
# used when the weather service is not available or returns an error
def _empty_weather(error="Weather data unavailable"):
    return {
        "available": False,
        "error": error,
        "city": "",
        "temperature": None,
        "feels_like": None,
        "humidity": None,
        "wind_speed": None,
        "condition": "",
        "description": "",
        "icon": "01d",
        "icon_url": "https://openweathermap.org/img/wn/01d@2x.png",
        "rain_probability": 0,
        "is_rainy": False,
        "recommendation_type": "Outdoor",
    }




# for getting recommended categories based on weather
def get_recommended_categories(weather_data):
    if weather_data.get("is_rainy"):
        return ["Museum", "Shopping", "Restaurant"]
    return ["Outdoor", "Heritage", "Restaurant"]


