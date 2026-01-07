# Le but sera de récolter les données de l'api de l'insee

# Imports des bibliothèques nécessaires
from bs4 import BeautifulSoup  # Pour parser du XML/HTML
import pandas as pd  # Pour créer et manipuler des tableaux de données
import requests  # Pour faire des requêtes HTTP

# URL de l'API INSEE contenant les données d'argent (indice en euros)
url = "https://api.insee.fr/series/BDM/data/SERIES_BDM/010002086?startPeriod=1990&endPeriod=2025"

try:
    # Étape 1: Faire une requête GET à l'URL de l'API
    # timeout=10 signifie qu'on attend maximum 10 secondes la réponse
    response = requests.get(url, timeout=10)
    
    # Vérifier si la requête a réussi (lève une exception si erreur HTTP)
    response.raise_for_status()
    
    # Étape 2: Parser le contenu XML retourné par l'API
    # 'xml' spécifie qu'on traite un document XML
    soup = BeautifulSoup(response.content, 'xml')
    
    # Chercher la balise <Series> dans le document XML
    # Elle contient toutes les infos générales et les observations
    series = soup.find('Series')
    
    # Vérifier qu'on a bien trouvé une série de données
    if series:
        # Étape 3: Afficher les informations de la série
        print("=" * 60)
        # Afficher le titre en français (attribut TITLE_FR de la balise Series)
        print(f"📊 {series['TITLE_FR']}")
        print("=" * 60)
        # Afficher l'unité de mesure (SO = Indice) et la fréquence (M = Mensuel)
        print(f"Unité: {series['UNIT_MEASURE']} | Fréquence: {series['FREQ']}")
        # Afficher la date de dernière mise à jour des données
        print(f"Dernière mise à jour: {series['LAST_UPDATE']}\n")
        
        # Étape 4: Créer une liste pour stocker les données
        donnees = []
        
        # Parcourir toutes les balises <Obs> (observations) dans la série
        # Chaque <Obs> représente une valeur pour une période donnée
        for obs in series.find_all('Obs'):
            # Ajouter un dictionnaire avec les infos de cette observation
            donnees.append({
                'Période': obs['TIME_PERIOD'],  # Ex: 2025-11
                'Valeur': float(obs['OBS_VALUE']),  # Valeur de l'indice (convertie en nombre)
                'Statut': obs['OBS_STATUS'],  # A = Valeur réelle
                'Qualité': obs['OBS_QUAL']  # DEF = Donnée définitive
            })
        
        # Étape 5: Créer un DataFrame pandas à partir de la liste de données
        # Un DataFrame est un tableau avec colonnes et lignes
        df = pd.DataFrame(donnees)
        
        # Afficher le DataFrame sous forme de tableau formaté
        # index=False pour ne pas afficher le numéro de ligne
        print(df.to_string(index=False))
        
        # Étape 6: Sauvegarder les données dans un fichier CSV
        # CSV = format texte avec données séparées par des virgules
        df.to_csv('donnees_insee.csv', index=False)
        print(f"\n✅ Données sauvegardées dans 'donnees_insee.csv'")
    else:
        # Si on n'a pas trouvé de série, afficher un message d'erreur
        print("❌ Aucune série trouvée")

# Gérer les erreurs de requête (pas de connexion, timeout, etc.)
except requests.exceptions.RequestException as e:
    print(f"❌ Erreur de connexion: {e}")

# Gérer toute autre erreur non prévue
except Exception as e:
    print(f"❌ Erreur: {e}")