import requests

def recuperer_meteo(ville):
    """Récupère la météo d'une ville"""
    url = "https://api.open-meteo.com/v1/forecast"
    
    params = {
        "latitude": 48.8566,
        "longitude": 2.3522,
        "current": "temperature_2m,weather_code"
    }
    
    response = requests.get(url, params=params)
    meteo = response.json()
    
    temp = meteo['current']['temperature_2m']
    print(f"Température: {temp}°C")
    return meteo

recuperer_meteo("Paris")