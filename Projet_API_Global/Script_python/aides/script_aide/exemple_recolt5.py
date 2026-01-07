import requests

url = "https://example.com"
response = requests.get(url)

# Étape 1: Vérifier que ça marche
if response.status_code == 200:
    # Étape 2: Récupérer le contenu HTML
    html = response.text
    print(html[:500])  # Affiche les 500 premiers caractères
    
    # Étape 3: Parser avec BeautifulSoup (optionnel)
    from bs4 import BeautifulSoup
    soupe = BeautifulSoup(html, 'html.parser')
    titres = soupe.find_all('h1')  # Récupérer tous les H1