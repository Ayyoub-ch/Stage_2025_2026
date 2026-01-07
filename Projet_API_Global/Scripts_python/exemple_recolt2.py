import requests

url = "https://api.github.com/search/repositories"

# Paramètres de recherche
parametres = {
    "q": "language:python",  # Chercher repos en Python
    "sort": "stars",         # Trier par étoiles
    "per_page": 5            # Limiter à 5 résultats
}

response = requests.get(url, params=parametres)

# Parcourir les résultats
for repo in response.json()['items']:
    print(f"{repo['name']} - {repo['stars']} ⭐")