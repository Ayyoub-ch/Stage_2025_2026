# ================================
# IMPORT DES BIBLIOTHÈQUES
# ================================

import requests    # Pour récupérer les données depuis l'API
import os          # Pour créer des dossiers et gérer les fichiers
import json        # Pour manipuler et sauvegarder les fichiers JSON
from datetime import datetime

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
seances={}
expos={}
for film in films:
    try:
        # Extraction des métadonnées principales
        titre = film.get("filmtitle", "Film_sans_titre").replace("/", "_").replace("\\", "_").upper().replace(":", "")
        film_id = film.get("filmid", "ID_Inconnu")
        cine_id = film.get("cineid", "Cine_Inconnu")
        departement = str(film.get("cinecp", "00"))[:1] if len(str(film.get("cinecp", "00"))) == 4 else str(film.get("cinecp", "00"))[:2]  # Les deux premiers chiffres du code postal
        date_sortie = film.get("showstart", "Date Inconnue")[:10] # Format AAAA-MM-JJ mettre le cas 01-9 en 01-09
        nom_cine = film.get("cinenom", "Cine_inconnu").replace("/", "_").replace("\\", "_")
        debut_seance = film.get("showstart", "Date Inconnue")[11:19]
        fin_seance = film.get("showend", "Date Inconnue")[11:19]
        heures_visionnage = {"DEBUT_SEANCE": debut_seance, "FIN_SEANCE": fin_seance } #, "NOM CINE": nom_cine, "JOUR_SEANCE": date_sortie

        key=(film_id, nom_cine, date_sortie)

        if key not in seances:
            seances[key] = []
        seances[key].append(heures_visionnage)


        # Gestion des dates d'exposition

        key_expo=(film_id, nom_cine, departement)

        date_obj = datetime.strptime(date_sortie, "%Y-%m-%d").date()

        if key_expo not in expos:
            expos[key_expo] = {"dates": set()}  # utiliser un set pour éviter les doublons

        expos[key_expo]["dates"].add(date_obj)

        
        dates = expos[key_expo]["dates"]
        debut_expo = min(dates)
        for date in dates:
            if date > debut_expo:
                date = max(dates)
                fin_expo = date
            else:
                fin_expo = debut_expo


        # Création du dossier du cinéma
        dossier_cine = os.path.join(DOSSIER_PRINCIPAL, departement, date_sortie)
        os.makedirs(dossier_cine, exist_ok=True)

        # Chemin complet du fichier JSON
        chemin_fichier = os.path.join(dossier_cine, f"{titre}.json")

        # ================================
        # MODIFICATION : transformer la durée en HHhMM
        # ================================
        duree_min = film.get("filmduration", 0)  # récupère la durée en minutes
        if duree_min:
            heures = duree_min // 60
            minutes = duree_min % 60
            duree_formatee = f"{heures}h{minutes:02d}"  # ex : 1h45
        else:
            duree_formatee = None  # ou "Inconnue"


        # Métadonnées et informations du film
        # Création du JSON final avec META et SEANCES
        metadata = {
            "DONNEES GENERALES": {
                "TITRE": titre, 
                "GENRE": film.get("filmgenre"), 
                "DUREE": duree_formatee, 
                "SHOW_URL": film.get("showurl"), 
                "ID_CINE": film.get("cineid"), 
                "NOM_CINE": nom_cine, 
                "ADRESSE_CINE": film.get("cineadresse"), 
                "CP_CINE": film.get("cinecp"), 
                "VILLE_CINE": film.get("cineville"), 
                "CAPACITE_CINE": film.get("auditoriumcapacity"), 
                "DATE_EXPOSITION": str(debut_expo), 
                "FIN_EXPOSITION": str(fin_expo),
            },
            "SEANCES": seances[key],
        }

        # Sauvegarde JSON
        with open(chemin_fichier, "w", encoding="utf-8") as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
        print(f"✅ Fichier créé : {chemin_fichier}")

    except Exception as e:
        print(f"❌ Erreur pour le film {titre} : {e}")
