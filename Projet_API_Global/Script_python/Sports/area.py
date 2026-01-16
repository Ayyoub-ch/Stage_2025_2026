import requests
import pprint
import time  # Ajout pour gérer le rate limiting

# Récupération des informations pour plusieurs zones géographiques

areas=[2081,2077]
for area in areas:
    url_area = f"https://api.football-data.org/v4/areas/{area}"
    headers = {"X-Auth-Token": "70228427e9454df9b59585c8462b4978"}

    response = requests.get(url_area, headers=headers)

    if response.status_code == 200:
        data = response.json()
        pprint.pprint(data)
    else:
        print("Erreur API:", response.status_code, response.text)
    time.sleep(5)