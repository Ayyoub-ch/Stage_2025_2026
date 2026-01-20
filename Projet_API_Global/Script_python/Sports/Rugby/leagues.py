import os
import requests
import pprint
import time
import json

DOSSIER_RACINE = "Rugby_API"
DOSSIER = "Leagues"
DOSSIER_FR = "France"
DOSSIER_MONDE = "World"
COUNTRY_FOLDERS = {
    "europe": "Europe",
    "france": "France",
}

leagues = ["europe", "france"]


# Récupération des compétitions
for country_param, country_folder in COUNTRY_FOLDERS.items():

    # Création du dossier country (World / France)
    chemin = os.path.join(DOSSIER_RACINE, DOSSIER, country_folder)
    os.makedirs(chemin, exist_ok=True)

    url_compet = f"https://v1.rugby.api-sports.io/leagues?search={country_param}"
    headers = {"x-apisports-key": "dc56c5bba70f6f222790a01874888304"}
    response = requests.get(url_compet, headers=headers)

    if response.status_code == 200:
        try:
            api_data = response.json()
            competitions = api_data.get("response", [])

            for comp in competitions:
                country_info = comp.get("country", {})
                seasons = comp.get("seasons", [])

                nom = comp.get("name", "unknown_league")

                data_json = {
                    "LEAGUE": {
                        "id": comp.get("id"),
                        "name": nom,
                        "type": comp.get("type"),
                    },
                    "COUNTRY": {
                        "name": country_info.get("name"),
                        "code": country_info.get("code"),
                    },
                    "SEASONS": seasons
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
            print(f"Erreur traitement ligues {country_param}: {e}")
    else:
        print("Erreur API:", response.status_code, response.text)