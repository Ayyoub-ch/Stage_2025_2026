import os
import requests
import pprint
import time
import json

DOSSIER_RACINE = "Football_API"
DOSSIER = "Zones"

# Création des dossiers UNE SEULE FOIS
chemin = os.path.join(DOSSIER_RACINE, DOSSIER)
os.makedirs(chemin, exist_ok=True)

# Récupération des informations pour plusieurs zones géographiques
areas = [2081, 2077]

headers = {"X-Auth-Token": "70228427e9454df9b59585c8462b4978"}

for area in areas:
    url_area = f"https://api.football-data.org/v4/areas/{area}"
    response = requests.get(url_area, headers=headers)

    if response.status_code == 200:
        try:
            data = response.json()
            nom = data.get("name", f"zone_{area}")

            pprint.pprint(data)

            # Sauvegarde JSON (comme Teams)
            fichier_json = os.path.join(
                chemin,
                f"{nom.replace(' ', '_')}.json" #_{area} pour avoir l'id aussi
            )

            with open(fichier_json, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

            print(f"Données sauvegardées : {fichier_json}")

        except Exception as e:
            print(f"Erreur traitement zone {area}: {e}")
    else:
        print("Erreur API:", response.status_code, response.text)

    time.sleep(5)
