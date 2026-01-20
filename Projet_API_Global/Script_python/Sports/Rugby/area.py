import os
import requests
import pprint
import time
import json

DOSSIER_RACINE = "Rugby_API"
DOSSIER = "Zones"

# Création des dossiers UNE SEULE FOIS
chemin = os.path.join(DOSSIER_RACINE, DOSSIER)
os.makedirs(chemin, exist_ok=True)

# Récupération des informations pour plusieurs zones géographiques

headers = {"x-apisports-key": "dc56c5bba70f6f222790a01874888304"}

url_area = f"https://v1.rugby.api-sports.io/countries?name=france"
response = requests.get(url_area, headers=headers)

if response.status_code == 200:
    try:
        data = response.json()
        nom = data.get("parameters", {}).get("name", "unknown_area")

        data_json={
            "NOM": nom,
        }

         # Sauvegarde JSON (comme Teams)
        fichier_json = os.path.join(
            chemin,
            f"{nom.replace(' ', '_')}.json" #_{area} pour avoir l'id aussi
        )

        with open(fichier_json, "w", encoding="utf-8") as f:
            json.dump(data_json, f, ensure_ascii=False, indent=4)

        print(f"Données sauvegardées : {fichier_json}")

    except Exception as e:
        print(f"Erreur traitement zone {nom}: {e}")

else:
    print("Erreur API:", response.status_code, response.text)

time.sleep(5)
