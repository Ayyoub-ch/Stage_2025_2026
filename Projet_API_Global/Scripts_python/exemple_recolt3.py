import requests

url = "https://jsonplaceholder.typicode.com/posts"

# Données à envoyer
donnees = {
    "title": "Mon titre",
    "body": "Mon contenu",
    "userId": 1
}

response = requests.post(url, json=donnees)

# Résultat
print(response.json())  # Affiche l'objet créé avec un ID