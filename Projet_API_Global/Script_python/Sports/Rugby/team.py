import requests
import time
import os
import json

DOSSIER_RACINE = "Rugby_API"
DOSSIER = "Teams"

chemin = os.path.join(DOSSIER_RACINE, DOSSIER)
os.makedirs(chemin, exist_ok=True)

headers = {
    "x-apisports-key": "dc56c5bba70f6f222790a01874888304"  # variable d'environnement
}

url_team = "https://v1.rugby.api-sports.io/teams?search=France"
response = requests.get(url_team, headers=headers)

if response.status_code == 200:
    try:
        api_data = response.json()
        teams = api_data.get("response", [])

        for team_data in teams:
            country_info = team_data.get("country", {})

            nom = team_data.get("name", "unknown_team")

            data_json = {
                "INFOS_EQUIPE": {
                    "id": team_data.get("id"),
                    "name": nom,
                    "code": team_data.get("code"),
                    "national": team_data.get("national"),
                    "founded": team_data.get("founded"),
                },
                "PAYS": {
                    "id": country_info.get("id"),
                    "name": country_info.get("name"),
                    "address": country_info.get("address"),
                    "code": country_info.get("code"),
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
