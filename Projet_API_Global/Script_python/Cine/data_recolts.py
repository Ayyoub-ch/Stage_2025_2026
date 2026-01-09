# ================================
# IMPORT DES BIBLIOTHÈQUES
# ================================

import requests    # Pour récupérer les données depuis l'API
import os          # Pour créer des dossiers et gérer les fichiers
import json        # Pour manipuler et sauvegarder les fichiers JSON
#from datetime import datetime

# ================================
# CONFIGURATION DES DOSSIERS
# ================================

# Dossier principal
DOSSIER_PRINCIPAL = "Cine"


# ================================
# URL DE L'API JSON
# ================================

url_api = (
    "https://data-cines-indes.koumoul.com/data-fair/api/v1/datasets/programmation-cinemas/lines?draft=false&size=10000&finalizedAt=2026-01-09T01:15:34.235Z&page=1&select=filmtitle,filmdirector,filmcast,filmstoryline,filmgenre,filmcountry,filmduration,showstart,showend,evenement,auditoriumnumber,filmversion,filmaudio,filmtrailer,filmposter,showid,filmid,showurl,cineid,cinenom,cineadresse,cinecp,cineville,description,auditoriumcapacity&format=json"
)

# ================================
# RÉCUPÉRATION DES DONNÉES
# ================================

try:
    response = requests.get(url_api, timeout=10)
    response.raise_for_status()  # Lève une erreur si problème réseau

    # Conversion de la réponse en JSON Python
    reponse_json = response.json()
    films = reponse_json.get("results", [])  # Récupère la liste des films
    print(f"✅ {len(films)} films récupérés depuis l'API")

except requests.exceptions.RequestException as e:
    print(f"❌ Erreur lors de la récupération des données : {e}")
    exit(1)  # On arrête le script en cas d'erreur réseau

# ================================
# TRAITEMENT DE CHAQUE FILM
# ================================ 

# installer wsl:  wsl --install Ubuntu-20.04

for film in films:
    try:
        # Extraction des métadonnées principales
        titre = film.get("filmtitle", "Film_sans_titre").replace("/", "_").replace("\\", "_")
        departement = str(film.get("cinecp", "00"))[:1] if len(str(film.get("cinecp", "00"))) == 4 else str(film.get("cinecp", "00"))[:2]  # Les deux premiers chiffres du code postal
        date_sortie = film.get("showstart", "Date Inconnue")[:10] # Format AAAA-MM-JJ mettre le cas 01-9 en 01-09
        nom_cine = film.get("cinenom", "Cine_inconnu").replace("/", "_").replace("\\", "_")

        # Création du dossier du cinéma
        dossier_cine = os.path.join(DOSSIER_PRINCIPAL, departement, date_sortie)
        os.makedirs(dossier_cine, exist_ok=True)

        # Chemin complet du fichier JSON
        chemin_fichier = os.path.join(dossier_cine, f"{titre}.json")

        # Métadonnées et informations du film
        metadata = {
            "TITRE": titre.upper().replace(":", " "),
            "GENRE": film.get("filmgenre"),
            "DUREE": film.get("filmduration"),
            "SHOW_URL": film.get("showurl"),
            #"DATE_EXPOSITION": min(film.get("showstart")) if film.get("showstart") else None,
            # "FIN_EXPOSITION": max(film.get("showend")) if film.get("showend") else None,
            "ID_CINE": film.get("cineid"),
            "NOM_CINE": nom_cine,
            "ADRESSE_CINE": film.get("cineadresse"),
            "CP_CINE": film.get("cinecp"),
            "VILLE_CINE": film.get("cineville"),
            "CAPACITE_CINE": film.get("auditoriumcapacity"),
            "DEBUT_SEANCE": film.get("showstart"),
            "FIN_SEANCE": film.get("showend")
        }

        # Sauvegarde en JSON
        with open(chemin_fichier, "w", encoding="utf-8") as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)

        print(f"✅ Fichier créé : {chemin_fichier}")

    except Exception as e:
        # Ici film est toujours un dict donc .get fonctionne
        print(f"❌ Erreur lors du traitement du film {film.get('filmtitle', 'INCONNU')}: {e}")
