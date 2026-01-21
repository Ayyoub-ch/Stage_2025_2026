import os
import requests
import pprint
import time
import json

DOSSIER_RACINE = "Banque_France_API"


# Création des dossiers UNE SEULE FOIS
chemin = os.path.join(DOSSIER_RACINE)
os.makedirs(chemin, exist_ok=True)

# Récupération des informations pour plusieurs zones géographiques

url= "https://webstat.banque-france.fr/api/explore/v2.1/catalog/datasets/observations/exports/json/?where=series_key+IN+%28%22ICP.M.FR.N.000000.4.ANR%22%29&order_by=-time_period_start&apikey=6a1179509ee33d99a799f02a521d4cbb7f422df4cc1a2676ef63f694"

response = requests.get(url)

if response.status_code == 200:
    try:
        data_list = response.json()  # data_list est une liste
        if isinstance(data_list, list) and len(data_list) > 0:
            data = data_list[0]  # prendre le premier dictionnaire
        else:
            data = {}

        for data in data_list:
            # observations_attributes_and_values est une chaîne JSON
            obs_raw = data.get("observations_attributes_and_values", "{}")
            obs_dict = json.loads(obs_raw)  # convertir en dictionnaire

            obs_conf = obs_dict.get("OBS_CONF", "")
            obs_status = obs_dict.get("OBS_STATUS", "")

            data_json = {
                "DATASET_ID": data.get("dataset_id", ""),
                "CLE_SERIE": data.get("series_key", ""),
                "TITRE": data.get("title_fr", ""),
                "PERIODE": data.get("time_period", ""),
                "PERIODE_DEBUT": data.get("time_period_start", ""),
                "PERIODE_FIN": data.get("time_period_end", ""),
                "VALEUR": data.get("obs_value", ""),
                "STATUT": data.get("obs_status", ""),
                "PUBLICATION_DATE": data.get("updated_at", ""),
                "OBSEVATION": {
                    "VALEUR": obs_conf,
                    "STATUT": obs_status,
                },
                "BASKETS": data.get("baskets", []),
                "GREATEST_UPDATED_AT": data.get("greatest_updated_at", ""),
                "SERIE_UPLOAD_AT": data.get("series_greatest_updated_at", ""),
                "LAST_THEMES_UPDATED_AT": data.get("last_themes_updated_at", ""),
                "Chemin": data.get("path_fr", "")
            }

            period_file = str(data.get("time_period", ""))+ ".json"
            annee = str(data.get("time_period_start", ""))[:4]
            chemin_period = os.path.join(chemin, annee)
            os.makedirs(chemin_period, exist_ok=True)

            # Sauvegarde JSON
            fichier_json = os.path.join(
                chemin_period,
                period_file.replace(' ', '_')
            )

            with open(fichier_json, "w", encoding="utf-8") as f:
                json.dump(data_json, f, ensure_ascii=False, indent=4)

            print(f"Données sauvegardées : {fichier_json}")

    except Exception as e:
        period_file=data.get("time_period", "")
        print(f"Erreur traitement zone {period_file}: {e}")

else:
    print("Erreur API:", response.status_code, response.text)

time.sleep(5)

