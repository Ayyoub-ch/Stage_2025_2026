import requests
import time
import os
import json

DOSSIER_RACINE = "Football_API"
DOSSIER = "Teams"

chemin = os.path.join(DOSSIER_RACINE, DOSSIER)
os.makedirs(chemin, exist_ok=True)

headers = {
    "x-apisports-key": "dc56c5bba70f6f222790a01874888304"  # variable d'environnement
}

url_team = "https://v3.football.api-sports.io/teams?country=France"
response = requests.get(url_team, headers=headers)

if response.status_code == 200:
    try:
        api_data = response.json()
        teams = api_data.get("response", [])

        for team_data in teams:
            team_info = team_data.get("team", {})
            venue_info = team_data.get("venue", {})

            nom = team_info.get("name", "unknown_team")

            data_json = {
                "INFOS_EQUIPE": {
                    "id": team_info.get("id"),
                    "name": nom,
                    "code": team_info.get("code"),
                    "national": team_info.get("national"),
                    "founded": team_info.get("founded"),
                    "country": team_info.get("country"),
                },
                "VENUE": {
                    "id": venue_info.get("id"),
                    "name": venue_info.get("name"),
                    "address": venue_info.get("address"),
                    "city": venue_info.get("city"),
                    "capacity": venue_info.get("capacity"),
                    "surface": venue_info.get("surface"),
                }
            }

            fichier_json = os.path.join(
                chemin,
                f"{nom.replace(' ', '_')}.json"
            )

            with open(fichier_json, "w", encoding="utf-8") as f:
                json.dump(data_json, f, ensure_ascii=False, indent=4)

            print(f"Données sauvegardées : {fichier_json}")

        time.sleep(5)

    except Exception as e:
        print("Erreur :", e)
else:
    print("Erreur API:", response.status_code, response.text)
