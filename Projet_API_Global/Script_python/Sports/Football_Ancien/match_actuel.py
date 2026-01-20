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

# Matchs actuels
url_matchs_actuels = "https://v3.football.api-sports.io/fixtures?live=all&timezone=Europe/london"
headers = {"x-apisports-key": "dc56c5bba70f6f222790a01874888304"}

response = requests.get(url_matchs_actuels, headers=headers)

if response.status_code == 200:
    try:
        data = response.json()
        matchs = data.get("response", [])

        for match in matchs:
            fixture= match.get("fixture", {})
            league= match.get("league", {})
            teams= match.get("teams", {})
            goals= match.get("goals", {})
            score= match.get("score", {})
            events= match.get("events", [])

            data_json = {
                "FIXTURE": {
                    "id": fixture.get("id"),
                    "referee": fixture.get("referee"),
                    "timezone": fixture.get("timezone"),
                    "date": fixture.get("date"),
                    "timestamp": fixture.get("timestamp"),
                    "periods": fixture.get("periods"),
                    "venue": fixture.get("venue"),
                    "status": fixture.get("status"),
                },
                "LEAGUE": {
                    "id": league.get("id"),
                    "name": league.get("name"),
                    "country": league.get("country"),
                    "logo": league.get("logo"),
                    "flag": league.get("flag"),
                    "season": league.get("season"),
                },
                "TEAMS": {
                    "home": teams.get("home", {}),
                    "away": teams.get("away", {}),
                },
                "GOALS": {
                    "home": goals.get("home"),
                    "away": goals.get("away"),
                },
                "SCORES": {
                    "halftime": score.get("halftime"),
                    "fulltime": score.get("fulltime"),
                },
                "EVENTS": events,
            }
            nom_fichier=teams.get("home", {}).get("name", "home")+"_VS_"+teams.get("away", {}).get("name", "away")+".json"

            # Sauvegarde JSON
            fichier_json = os.path.join(
                chemin,
                nom_fichier
            )

            with open(fichier_json, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print(f"Données sauvegardées : {fichier_json}")

    except Exception as e:
        print(f"Erreur traitement matchs: {e}")
else:
    print("Erreur API:", response.status_code, response.text)

time.sleep(5)