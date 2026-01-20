import os
import requests
import pprint
import json
import time

DOSSIER_RACINE = "Football_API"
DOSSIER = "Competition Standings"

# Création des dossiers UNE SEULE FOIS
chemin = os.path.join(DOSSIER_RACINE, DOSSIER)
os.makedirs(chemin, exist_ok=True)

# Récupération des classements pour plusieurs compétitions
leagues = [2015, 2142, 2018, 2146, 2154, 2001, 2157, 2007]
# Ligue 1, Ligue 2, Euro, Europa League, Conference League, Champions League, Supercup, WC Qualif UEFA

headers = {"X-Auth-Token": "70228427e9454df9b59585c8462b4978"}

for league in leagues:
    url_compet = f"https://api.football-data.org/v4/competitions/{league}/standings"
    response = requests.get(url_compet, headers=headers)

    if response.status_code == 200:
        try:
            data = response.json()
            nom = data.get("competition", {}).get("name", f"competition_{league}")

            pprint.pprint(data)

            # Sauvegarde JSON
            fichier_json = os.path.join(
                chemin,
                f"{nom.replace(' ', '_')}.json" #_{league} pour avoir l'id aussi
            )

            with open(fichier_json, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

            print(f"Données sauvegardées : {fichier_json}")

        except Exception as e:
            print(f"Erreur traitement standings compétition {league}: {e}")
    else:
        print("Erreur API:", response.status_code, response.text)

    # Pause pour éviter le rate limiting
    time.sleep(5)
