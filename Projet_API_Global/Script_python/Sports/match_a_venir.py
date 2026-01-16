import requests
import pprint

# Récupération des matchs à venir en France et en Europe

url_match_a_venir = "https://api.football-data.org/v4/matches?status=SCHEDULED"

headers = {"X-Auth-Token": "70228427e9454df9b59585c8462b4978"}

response = requests.get(url_match_a_venir, headers=headers)

if response.status_code == 200:
    data = response.json()
    for match in data.get("matches", []):
        if match.get("area", {}).get("id") == 2081 or match.get("area", {}).get("id") == 2077:
            #or match.get("area", {}).get("id") == 2077 ça ne fonctionne pas parce qu'il n'y en a pas de match à venir en Europe
            pprint.pprint(match)
else:
    print("Erreur API:", response.status_code, response.text)