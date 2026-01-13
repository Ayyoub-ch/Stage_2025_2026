import sys
import requests
import os
import json
from datetime import datetime

# ================================
# CONFIGURATION ET SETUP
# ================================
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

DOSSIER_PRINCIPAL = "Cine"
url_api = (
    "https://data-cines-indes.koumoul.com/data-fair/api/v1/datasets/programmation-cinemas/lines?"
    "draft=false&size=10000&finalizedAt=2026-01-09T01:15:34.235Z&page=1&format=json"
)

# ================================
# 1. RÉCUPÉRATION DES DONNÉES
# ================================
try:
    response = requests.get(url_api, timeout=600)
    response.raise_for_status()
    films_data = response.json().get("results", [])
    print(f"✅ {len(films_data)} lignes récupérées depuis l'API")
except Exception as e:
    print(f"❌ Erreur lors de la récupération : {e}")
    exit(1)

# ================================
# 2. COLLECTE ET ANALYSE
# ================================
seances_par_jour = {}  # Stocke les listes de séances
expos_globales = {}    # Stocke toutes les dates par (film, ciné) pour calculer Min/Max
donnees_films = {}     # Stocke les métadonnées pour l'écriture finale

print("⏳ Analyse des périodes d'exposition...")

for film in films_data:
    try:
        film_id = film.get("filmid", "ID_Inconnu")
        cine_id = film.get("cineid", "Cine_Inconnu")
        cp = str(film.get("cinecp", "00"))
        
        # Calcul du département (gestion CP à 4 ou 5 chiffres)
        departement = cp[:1] if len(cp) == 4 else cp[:2]
        
        # Extraction et conversion de la date
        raw_start = film.get("showstart", "")
        if not raw_start or len(raw_start) < 10:
            continue
            
        date_sortie = raw_start[:10]
        date_obj = datetime.strptime(date_sortie, "%Y-%m-%d").date()

        # Clés de regroupement
        key_jour = (film_id, cine_id, date_sortie)
        key_expo = (film_id, cine_id, departement)

        # 1. On accumule les séances pour ce jour précis
        if key_jour not in seances_par_jour:
            seances_par_jour[key_jour] = []
        
        seances_par_jour[key_jour].append({
            "DEBUT_SEANCE": raw_start[11:19],
            "FIN_SEANCE": film.get("showend", "Inconnue")[11:19]
        })

        # 2. On stocke la date pour le calcul global du début/fin d'expo
        if key_expo not in expos_globales:
            expos_globales[key_expo] = set()
        expos_globales[key_expo].add(date_obj)

        # 3. On garde les infos générales pour ce jour (une seule fois suffit)
        if key_jour not in donnees_films:
            donnees_films[key_jour] = {
                "film": film,
                "dept": departement
            }

    except Exception as e:
        continue

# ================================
# 3. GÉNÉRATION DES FICHIERS JSON
# ================================
print(f"📂 Écriture des fichiers dans le dossier '{DOSSIER_PRINCIPAL}'...")

for key_jour, info in donnees_films.items():
    try:
        film_id, cine_id, date_str = key_jour
        film = info["film"]
        dept = info["dept"]
        
        # Récupération des dates d'exposition réelles
        dates_film_cine = expos_globales[(film_id, cine_id, dept)]
        debut_expo = min(dates_film_cine)
        fin_expo = max(dates_film_cine)

        # Formatage de la durée
        duree_min = film.get("filmduration", 0)
        duree_formatee = f"{duree_min // 60}h{duree_min % 60:02d}" if duree_min else None

        # Nettoyage du titre pour le nom de fichier
        titre_propre = film.get("filmtitle", "SANS_TITRE").replace("/", "_").replace("\\", "_").upper().replace(":", "")
        nom_cine_propre = film.get("cinenom", "Cine_inconnu").replace("/", "_").replace("\\", "_")

        # Construction du dictionnaire final avec TOUTES les données
        metadata = {
            "DONNEES GENERALES": {
                "TITRE": titre_propre,
                "GENRE": film.get("filmgenre"),
                "DUREE": duree_formatee,
                "SHOW_URL": film.get("showurl"),
                "ID_CINE": cine_id,
                "NOM_CINE": nom_cine_propre,
                "ADRESSE_CINE": film.get("cineadresse"),
                "CP_CINE": film.get("cinecp"),
                "VILLE_CINE": film.get("cineville"),
                "CAPACITE_CINE": film.get("auditoriumcapacity"),
                "DATE_EXPOSITION": str(debut_expo),
                "FIN_EXPOSITION": str(fin_expo),
            },
            "SEANCES": seances_par_jour[key_jour],
        }

        # Création du dossier : Cine / Dept / Date
        chemin_dossier = os.path.join(DOSSIER_PRINCIPAL, dept, date_str)
        os.makedirs(chemin_dossier, exist_ok=True)

        # Sauvegarde
        chemin_fichier = os.path.join(chemin_dossier, f"{titre_propre}.json")
        with open(chemin_fichier, "w", encoding="utf-8") as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)

    except Exception as e:
        print(f"❌ Erreur lors de l'écriture de {key_jour} : {e}")

print(f"✨ Opération terminée avec succès.")