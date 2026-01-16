import requests
import pprint
import time  # Ajout pour gérer le rate limiting

# Récupération des compétitions en France et en Europe

url_compet = "https://api.football-data.org/v4/competitions"
headers = {"X-Auth-Token": "70228427e9454df9b59585c8462b4978"}

response = requests.get(url_compet, headers=headers)

if response.status_code == 200:
    data = response.json()
    competitions_france_europe = [
        c for c in data.get("competitions", [])
        if c.get("area", {}).get("name") == "France" or c.get("area", {}).get("name") == "Europe"
    ]
    pprint.pprint(competitions_france_europe)
else:
    print("Erreur API:", response.status_code, response.text)
time.sleep(5)
