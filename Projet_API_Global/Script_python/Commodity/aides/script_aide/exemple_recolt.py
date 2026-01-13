import requests

# Étape 1: Faire une requête GET à une URL
url = "https://api.github.com/users/github"
response = requests.get(url)

# Étape 2: Vérifier le statut (200 = succès)
print(response.status_code)  # Affiche: 200

# Étape 3: Récupérer le contenu en JSON
donnees = response.json()
print(donnees['login'])  # Affiche: github
print(donnees['public_repos'])  # Nombre de repos publics