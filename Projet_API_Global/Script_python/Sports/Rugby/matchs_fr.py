import os
import requests
import pprint
import json
import time

DOSSIER_RACINE = "Rugby_API"
DOSSIER = "Matchs de la France"

# Création des dossiers UNE SEULE FOIS
chemin = os.path.join(DOSSIER_RACINE, DOSSIER)
os.makedirs(chemin, exist_ok=True)

id_france=387 
id_teams=[465, 461, 467, 386, 388, 391, 390]  
# Nouvelle-Zélande 465, Australie 461, Afrique du Sud 467, Angleterre 386, Irlande 388, Pays de Galles 391, Écosse 390

headers = {"x-apisports-key": "dc56c5bba70f6f222790a01874888304"}
# Matchs de la France
for id_team in id_teams:
    url_matchs_fr = f"https://v1.rugby.api-sports.io/games/h2h?h2h={id_france}-{id_team}"
    

    response = requests.get(url_matchs_fr, headers=headers)

    if response.status_code == 200:
        try:
            data = response.json()
            matchs = data.get("response", [])

            for match in matchs:
                id= match.get("id", {})
                date= match.get("date", {})
                temps= match.get("time", {})
                timezone= match.get("timezone", {})
                statut= match.get("statut", {})

                data_json = {
                    "MATCH": {
                        "id": id,
                        "date": date,
                        "time": temps,
                        "timezone": timezone,
                        "status": statut,
                    },
                    "COUNTRY": {
                        "id": match.get("country", {}).get("id"),
                        "name": match.get("country", {}).get("name"),
                    },
                    "LEAGUE": {
                        "id": match.get("league", {}).get("id"),
                        "name": match.get("league", {}).get("name"),
                        "type": match.get("league", {}).get("type"),
                        "season": match.get("league", {}).get("season"),
                    },
                    "TEAMS": {
                        "home":  match.get("teams", {}).get("home", {}),
                        "away": match.get("teams", {}).get("away", {}),
                    },
                    "SCORES": {
                        "home": match.get("scores", {}).get("home"),
                        "away": match.get("scores", {}).get("away"),
                    },
                    "PERIODES": {
                        "halftime": match.get("scores", {}).get("halftime"),
                        "fulltime": match.get("scores", {}).get("fulltime"),
                    },
                }
                nom_fichier=match.get("teams", {}).get("home", {}).get("name", "home")+"_VS_"+match.get("teams", {}).get("away", {}).get("name", "away")+"_"+date[:4]+".json"

                # Sauvegarde JSON
                fichier_json = os.path.join(
                    chemin,
                    nom_fichier
                )

                with open(fichier_json, "w", encoding="utf-8") as f:
                    json.dump(data_json, f, ensure_ascii=False, indent=4)
                print(f"Données sauvegardées : {fichier_json}")

        except Exception as e:
            print(f"Erreur traitement matchs: {e}")
    else:
        print("Erreur API:", response.status_code, response.text)

    time.sleep(5)