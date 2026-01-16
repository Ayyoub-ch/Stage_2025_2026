import requests
import pprint
import time  # Ajout pour gérer le rate limiting
# Récupération des informations pour plusieurs compétitions
leagues=[2015,2142,2018,2146,2154,2001,2157,2007] 
#ligue 1, ligue 2, European Championship, UEFA Europa League, UEFA Conference League, UEFA Champions League, Supercup, WC Qualification UEFA
for league in leagues:
     url_compet = f"https://api.football-data.org/v4/competitions/{league}"
     headers = {"X-Auth-Token": "70228427e9454df9b59585c8462b4978"}

     response = requests.get(url_compet, headers=headers)

     if response.status_code == 200:
         data = response.json()
         pprint.pprint(data)
     else:
         print("Erreur API:", response.status_code, response.text)
     
     # Pause de 2 secondes entre chaque requête pour éviter le rate limiting (erreur 429)
     time.sleep(5)