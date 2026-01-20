import os
import requests
import pprint
import json
import time

DOSSIER_RACINE = "Football_API"
DOSSIER = "Matchs Actuels"

# Création des dossiers UNE SEULE FOIS
chemin = os.path.join(DOSSIER_RACINE, DOSSIER)
os.makedirs(chemin, exist_ok=True)

# Matchs actuels de France et d'Europe
url_matchs_actuels = "https://api.football-data.org/v4/matches"
headers = {"X-Auth-Token": "70228427e9454df9b59585c8462b4978"}

response = requests.get(url_matchs_actuels, headers=headers)

if response.status_code == 200:
    try:
        data = response.json()

        matchs_france_europe = [
            match for match in data.get("matches", [])
            if match.get("area", {}).get("id") in (2081, 2077)
        ]

        pprint.pprint(matchs_france_europe)

        # Sauvegarde JSON
        fichier_json = os.path.join(
            chemin,
            "matchs_actuels_france_europe.json"
        )

        with open(fichier_json, "w", encoding="utf-8") as f:
            json.dump(matchs_france_europe, f, ensure_ascii=False, indent=4)

        print(f"Données sauvegardées : {fichier_json}")

    except Exception as e:
        print(f"Erreur traitement matchs: {e}")
else:
    print("Erreur API:", response.status_code, response.text)

time.sleep(5)
