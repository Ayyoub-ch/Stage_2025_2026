# ================================
# IMPORT DES BIBLIOTHÈQUES
# ================================

import logging
import requests    # Pour récupérer les données depuis l'API
import os          # Pour créer des dossiers et gérer les fichiers
import json        # Pour manipuler et sauvegarder les fichiers JSON
from datetime import datetime, timedelta # Pour gérer les dates

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
# Regrouper les films par clé unique pour traiter les doublons correctement
# ================================

seances = {}
expos = {}

# Regrouper les films par (film_id, cine_id, departement) pour traiter chaque groupe en ordre
films_par_groupe = {}

for film in films:
    film_id = film.get("filmid", "ID_Inconnu")
    cine_id = film.get("cineid", "Cine_Inconnu")
    departement = str(film.get("cinecp", "00"))[:1] if len(str(film.get("cinecp", "00"))) == 4 else str(film.get("cinecp", "00"))[:2]
    key_expo = (film_id, cine_id, departement)
    
    if key_expo not in films_par_groupe:
        films_par_groupe[key_expo] = []
    films_par_groupe[key_expo].append(film)

# ================================
# Traiter les films groupés en extraisant les dates min/max AVANT d'écrire les JSON
# ================================

for key_expo, films_groupe in films_par_groupe.items():
    film_id, cine_id, departement = key_expo
    
    # Trouver les dates min et max pour ce groupe
    dates_groupe = []
    for film in films_groupe:
        date_sortie = film.get("showstart", "Date Inconnue")[:10]
        try:
            date_obj = datetime.strptime(date_sortie, "%Y-%m-%d").date()
            dates_groupe.append(date_obj)
        except:
            pass
    
    if dates_groupe:
        debut_expo_groupe = min(dates_groupe)
        fin_expo_groupe = max(dates_groupe)
    else:
        debut_expo_groupe = None
        fin_expo_groupe = None
    
    # Traiter chaque film du groupe
    for film in films_groupe:
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

            key=(film_id, cine_id, date_sortie)

            if key not in seances:
                seances[key] = []
            seances[key].append(heures_visionnage)


            # Les dates d'exposition ont déjà été calculées pour tout le groupe
            # Utiliser les valeurs du groupe (pas besoin de réappeler)
            debut_expo = debut_expo_groupe
            fin_expo = fin_expo_groupe


            # Création du dossier du cinéma
            dossier_cine = os.path.join(DOSSIER_PRINCIPAL, departement, date_sortie)
            os.makedirs(dossier_cine, exist_ok=True)

            # Chemin complet du fichier JSON
            chemin_fichier = os.path.join(dossier_cine, f"{titre}.json")

            # ================================
            # MODIFICATION : transformer la durée en HHhMM
            # ================================
            duree = film.get("filmduration")

            if duree >= 300:
                td = timedelta(seconds=duree)

                total_seconds = int(td.total_seconds())
                heures, reste = divmod(total_seconds, 3600)
                minutes, secondes = divmod(reste, 60)

                duree_formatee = f"{heures}:{minutes:02d}:{secondes:02d}"

            elif duree < 300:
                duree=timedelta(minutes=duree)
                duree_formatee = f"{duree}"
            


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
            #logging.info(f"Fichier créé : {chemin_fichier}")

        except Exception as e:
            print(f"❌ Erreur pour le groupe {key_expo} : {e}")
