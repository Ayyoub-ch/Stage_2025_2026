import requests

url = "https://httpbin.org/status/404"

try:
    response = requests.get(url, timeout=5)  # Timeout de 5 secondes
    response.raise_for_status()  # Lève une exception si erreur (404, 500, etc.)
except requests.exceptions.HTTPError as e:
    print(f"Erreur HTTP: {e}")
except requests.exceptions.Timeout:
    print("La requête a expiré")
except requests.exceptions.RequestException as e:
    print(f"Erreur: {e}")