# ================================
# IMPORTS DES BIBLIOTHÈQUES
# ================================

from bs4 import BeautifulSoup  # Permet de parser et parcourir du XML (réponse de l'API INSEE)
import pandas as pd            # Bibliothèque d'analyse de données (non utilisée ici, mais utile ensuite)
import requests                # Permet d'envoyer des requêtes HTTP vers l'API
import os                      # Permet de gérer les fichiers et dossiers du système
import json                    # Permet d'écrire des données Python en format JSON


# ================================
# CRÉATION DU DOSSIER DE SORTIE
# ================================

# Nom du dossier où seront stockés les fichiers JSON
DOSSIER_SORTIE = "donnees_insee"

# Crée le dossier s'il n'existe pas déjà
# exist_ok=True évite une erreur si le dossier existe déjà
os.makedirs(DOSSIER_SORTIE, exist_ok=True)


# ================================
# DÉFINITION DES MATÉRIAUX ET DES URLS INSEE
# ================================

# Dictionnaire associant chaque matériau à son URL API INSEE
# La clé sert pour le nom du fichier
# La valeur est l'endpoint de l'API
materiaux = {
    "argent": "https://api.insee.fr/series/BDM/data/SERIES_BDM/010002086?startPeriod=1990&endPeriod=2025",
    "petrole_brut": "https://api.insee.fr/series/BDM/data/SERIES_BDM/010002091?startPeriod=1990&endPeriod=2025",
    "aluminium": "https://api.insee.fr/series/BDM/data/SERIES_BDM/010002093?startPeriod=1990&endPeriod=2025",
    "cuivre": "https://api.insee.fr/series/BDM/data/SERIES_BDM/010002094?startPeriod=1990&endPeriod=2025",
    "etain": "https://api.insee.fr/series/BDM/data/SERIES_BDM/010002095?startPeriod=1990&endPeriod=2025",
    "plomb": "https://api.insee.fr/series/BDM/data/SERIES_BDM/010002097?startPeriod=1990&endPeriod=2025",
    "zinc": "https://api.insee.fr/series/BDM/data/SERIES_BDM/010002098?startPeriod=1990&endPeriod=2025",
    "or": "https://api.insee.fr/series/BDM/data/SERIES_BDM/010002100?startPeriod=1990&endPeriod=2025",
    "platine": "https://api.insee.fr/series/BDM/data/SERIES_BDM/010002101?startPeriod=1990&endPeriod=2025",
    "cobalt": "https://api.insee.fr/series/BDM/data/SERIES_BDM/010767331?startPeriod=1990&endPeriod=2025"
}


# ================================
# BOUCLE PRINCIPALE : TRAITEMENT DE CHAQUE MATÉRIAU
# ================================

# Parcourt chaque couple (materiau, url) du dictionnaire
for materiau, url in materiaux.items():
    try:
        # Affiche le matériau en cours de traitement
        print(f"\n🔎 Traitement : {materiau.upper()}")

        # ----------------------------
        # REQUÊTE HTTP VERS L'API INSEE
        # ----------------------------

        # Envoie une requête GET à l'URL
        # timeout=10 empêche le script de bloquer trop longtemps
        response = requests.get(url, timeout=10)

        # Déclenche une exception si le code HTTP indique une erreur (404, 500, etc.)
        response.raise_for_status()


        # ----------------------------
        # PARSING DU XML
        # ----------------------------

        # Transforme le XML brut en structure navigable
        soup = BeautifulSoup(response.content, "xml")

        # Recherche la balise <Series> (contient métadonnées + observations)
        series = soup.find("Series")

        # Si aucune série n'est trouvée, on passe au matériau suivant
        if not series:
            print(f"❌ Série introuvable pour {materiau}")
            continue


        # ----------------------------
        # EXTRACTION DES MÉTADONNÉES
        # ----------------------------

        # Les métadonnées sont stockées comme attributs de la balise <Series>
        metadata = {
            "IDBANK": series.get("IDBANK"),
            "FREQ": series.get("FREQ"),
            "TITLE_FR": series.get("TITLE_FR"),
            "TITLE_EN": series.get("TITLE_EN"),
            "LAST_UPDATE": series.get("LAST_UPDATE"),
            "UNIT_MEASURE": series.get("UNIT_MEASURE"),
            "UNIT_MULT": series.get("UNIT_MULT"),
            "REF_AREA": series.get("REF_AREA"),
            "DECIMALS": series.get("DECIMALS")
        }


        # ----------------------------
        # EXTRACTION DES DONNÉES (OBSERVATIONS)
        # ----------------------------

        # Liste qui contiendra toutes les observations de la série
        donnees = []

        # Chaque balise <Obs> correspond à une période (mensuelle ici)
        for obs in series.find_all("Obs"):
            donnees.append({
                "Periode": obs["TIME_PERIOD"],          # Ex : 2025-01
                "Valeur": float(obs["OBS_VALUE"]),      # Conversion en nombre
                "Statut": obs["OBS_STATUS"],             # A = valeur observée
                "Qualite": obs["OBS_QUAL"]               # DEF = donnée définitive
            })


        # ----------------------------
        # STRUCTURE FINALE DU JSON
        # ----------------------------

        # On regroupe métadonnées et données dans un seul objet
        resultat = {
            "metadata": metadata,
            "data": donnees
        }


        # ----------------------------
        # SAUVEGARDE DU FICHIER JSON
        # ----------------------------

        # Construction du chemin du fichier (compatible tous OS)
        chemin_fichier = os.path.join(DOSSIER_SORTIE, f"{materiau}.json")

        # Écriture du fichier JSON
        with open(chemin_fichier, "w", encoding="utf-8") as f:
            # ensure_ascii=False conserve les accents
            # indent=2 rend le fichier lisible
            json.dump(resultat, f, ensure_ascii=False, indent=2)

        # Confirmation de création du fichier
        print(f"✅ Fichier créé : {chemin_fichier}")


    # ----------------------------
    # GESTION DES ERREURS
    # ----------------------------

    # Erreurs liées au réseau ou à l'API
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur réseau ({materiau}) : {e}")

    # Toute autre erreur inattendue
    except Exception as e:
        print(f"❌ Erreur ({materiau}) : {e}")
