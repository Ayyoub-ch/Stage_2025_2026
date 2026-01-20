import requests
import pprint
import time
import os
import json

DOSSIER_RACINE = "Football_API"
DOSSIER = "Teams"

# Création des dossiers UNE SEULE FOIS
chemin = os.path.join(DOSSIER_RACINE, DOSSIER)
os.makedirs(chemin, exist_ok=True)

teams = range(511, 547)

headers = {"X-Auth-Token": "70228427e9454df9b59585c8462b4978"}

for team in teams:
    url_team = f"https://api.football-data.org/v4/teams/{team}"
    response = requests.get(url_team, headers=headers)

    if response.status_code == 200:
        try:
            data = response.json()
            nom = data.get("name", f"equipe_{team}")

            # Filtre France
            if data.get("area", {}).get("id") == 2081:
                pprint.pprint(data)

                fichier_json = os.path.join(
                    chemin,
                    f"{nom.replace(' ', '_')}.json" #_{team} pour avoir l'id aussi
                )

                with open(fichier_json, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)

                print(f"Données sauvegardées : {fichier_json}")

        except ValueError:
            print(f"Erreur JSON pour l'équipe {team}")
        except Exception as e:
            print(f"Erreur pour l'équipe {team}: {e}")
    else:
        print("Erreur API:", response.status_code, response.text)

    time.sleep(5)
