import os
import requests
import pprint
import time
import json

DOSSIER_RACINE = "Football_API"
DOSSIER = "Competitions"

# Création des dossiers UNE SEULE FOIS
chemin = os.path.join(DOSSIER_RACINE, DOSSIER)
os.makedirs(chemin, exist_ok=True)

# Récupération des compétitions
url_compet = "https://api.football-data.org/v4/competitions"
headers = {"X-Auth-Token": "70228427e9454df9b59585c8462b4978"}

response = requests.get(url_compet, headers=headers)

if response.status_code == 200:
    try:
        data = response.json()

        competitions_france_europe = [
            c for c in data.get("competitions", [])
            if c.get("area", {}).get("name") in ("France", "Europe")
        ]

        pprint.pprint(competitions_france_europe)

        # Sauvegarde JSON
        fichier_json = os.path.join(
            chemin,
            "competitions_france_europe.json"
        )

        with open(fichier_json, "w", encoding="utf-8") as f:
            json.dump(competitions_france_europe, f, ensure_ascii=False, indent=4)

        print(f"Données sauvegardées : {fichier_json}")

    except Exception as e:
        print(f"Erreur traitement compétitions: {e}")
else:
    print("Erreur API:", response.status_code, response.text)

time.sleep(5)
