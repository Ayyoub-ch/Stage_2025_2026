import requests
import pprint
#matchs actuels de France et d'Europe
url_matchs_actuels = "https://api.football-data.org/v4/matches"

headers = {"X-Auth-Token": "70228427e9454df9b59585c8462b4978"}

response = requests.get(url_matchs_actuels, headers=headers)
if response.status_code == 200:
    data = response.json()
    
    # DIFFÉRENCE 1: Le code précédent cherchait "area" à la racine de la réponse (data.get("area"))
    # or "area" n'existe que DANS chaque match, pas au niveau racine.
    # Maintenant on boucle sur data.get("matches", []) pour accéder à chaque match individuellement
    
    # DIFFÉRENCE 2: L'ID est un nombre (2081), pas une chaîne ("2081")
    # Le code précédent comparait avec "2081" (string) ce qui était toujours False
    
    for match in data.get("matches", []):
        if match.get("area", {}).get("id") == 2081 or match.get("area", {}).get("id") == 2077:
            pprint.pprint(match)
else:
    print("Erreur API:", response.status_code, response.text)