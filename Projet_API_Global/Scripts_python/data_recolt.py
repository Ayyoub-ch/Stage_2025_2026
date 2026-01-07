# Le but sera de récolter les données de l'api de l'insee


import requests

# Étape 1: Faire une requête GET à l'URL
url = "https://api.insee.fr/series/BDM/data/SERIES_BDM/010002086?startPeriod=1990&endPeriod=2025&includeHistory=true&updatedAfter=2025-11-29"
response = requests.get(url)

# Étape 2: Vérifier le statut (200 = succès)
print(response.status_code)  # Affiche: 200

# Étape 3: Récupérer le contenu en JSON
#donnees = response.json()
#print(donnees['IDBANK'])  # ID de la banque de données
#print(donnees['FREQ'])  # Fréquence 
#print(donnees['TITLE_FR'])  # Titre en français
#print(donnees['TITLE_EN'])  # Titre en anglais
#print(donnees['LAST_UPDATE'])  # Dernière mise à jour
#print(donnees['UNIT_MEASURE'])  # Unité de mesure
#print(donnees['UNIT_MULT'])  # Multiplicateur d'unité
#print(donnees['REF_AREA'])  # Zone de référence
#print(donnees['DECIMALS'])  # Décimales

# Étape 4: Parcourir les données temporelles
#for data_point in donnees['OBS']:
#    print(f"Année: {data_point['TIME_PERIOD']}, Valeur: {data_point['OBS_VALUE']}, Statut: {data_point.get('OBS_STATUS', 'N/A')}, Qualité: {data_point.get('OBS_QUAL', 'N/A')}, Type: {data_point.get('OBS_TYPE', 'N/A')}")