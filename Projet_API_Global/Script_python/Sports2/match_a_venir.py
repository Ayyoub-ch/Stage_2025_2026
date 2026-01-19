import os
import requests
import pprint
import json
import time

DOSSIER_RACINE = "Football_API"
DOSSIER = "Matchs a Venir"

# Création des dossiers UNE SEULE FOIS
chemin = os.path.join(DOSSIER_RACINE, DOSSIER)
os.makedirs(chemin, exist_ok=True)

# Récupération des matchs à venir (France / Europe)
url_match_a_venir = "https://api.football-data.org/v4/matches?status=SCHEDULED"
headers = {"x-apisports-key": "dc56c5bba70f6f222790a01874888304"}

response = requests.get(url_match_a_venir, headers=headers)

if response.status_code == 200:
    try:
        data = response.json()
        matchs_a_venir = data.get("matches")

        # matchs_a_venir = [
        #     match for match in data.get("matches", [])
        #     if match.get("area", {}).get("id") in (2081, 2077)
        # ]

        # pprint.pprint(matchs_a_venir)

        # Sauvegarde JSON
        fichier_json = os.path.join(
            chemin,
            "matchs_a_venir.json" #_france_europe
        )

        with open(fichier_json, "w", encoding="utf-8") as f:
            json.dump(matchs_a_venir, f, ensure_ascii=False, indent=4)

        print(f"Données sauvegardées : {fichier_json}")

    except Exception as e:
        print(f"Erreur traitement matchs à venir: {e}")
else:
    print("Erreur API:", response.status_code, response.text)

time.sleep(5)
