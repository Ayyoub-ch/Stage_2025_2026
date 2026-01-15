import requests
import os
import json
import re



DOSSIER_PRINCIPAL = "Festivals"
url_api = (
    "https://www.data.gouv.fr/api/1/datasets/r/1270f4ef-61c8-4b6d-8f45-3afa17b589e7"
)

# ================================
# 1. RÉCUPÉRATION DES DONNÉES
# ================================
try:
    response = requests.get(url_api, timeout=600)
    response.raise_for_status()
    json_data = response.json()
    festivals_data = json_data
    print(f"✅ {len(festivals_data)} lignes récupérées depuis l'API")
except Exception as e:
    print(f"❌ Erreur lors de la récupération : {e}")
    exit(1)

# ================================
# 2. COLLECTE ET ANALYSE
# ================================
sous_categories = {}
for festival in festivals_data:
    try:

        # Nettoyer le titre (supprimer les caractères invalides pour Windows)
        titre = festival.get("nom_du_festival", "Titre_Inconnu")
        titre = re.sub(r'[?\"<>|*:/\\]', "", titre).strip()
        if not titre:
            titre = "Titre_Inconnu"
        
        # Extraire l'année (gérer les dates complètes comme "01/01/2003 00:00")
        annee_brute = festival.get("annee_de_creation_du_festival", "Annee_Inconnue")
        match_annee = re.search(r'\d{4}', str(annee_brute))
        annee_festival = match_annee.group() if match_annee else "Annee_Inconnue"
        
        adresse_postale = festival.get("adresse_postale", "Adresse_Inconnue") or "Adresse_Inconnue"
        complement = festival.get("complement_d_adresse_facultatif") or ""
        adresse_complete = adresse_postale + (", " + complement if complement else "")
        # Calcul du département (gestion CP à 4 ou 5 chiffres)
        cp = str(festival.get("code_postal_de_la_commune_principale_de_deroulement", "00"))
        if cp.isdigit() or re.search(r'\d{2}', cp):
            departement = cp[:1] if len(cp) == 4 else cp[:2]
        else:
            departement = "Non répertorié"
        
        # Gestion des codes postaux complémentaires
        codes_postaux_raw = festival.get("code_postal_de_la_commune_principale_de_deroulement")

        if len(codes_postaux_raw)>5 and "," in codes_postaux_raw:
            codes_postaux = [code.strip() for code in codes_postaux_raw.split(",") if code.strip()]
        else:
            codes_postaux = []

        # Gestion des sous-catégories
        sous_categories={"SOUS_CATEGORIE_SPECTACLE_VIVANT": festival.get("sous_categorie_spectacle_vivant"),
                         "SOUS_CATEGORIE_MUSIQUE": festival.get("sous_categorie_musique"),
                         "SOUS_CATEGORIE_MUSIQUE_CNM": festival.get("sous_categorie_musique_cnm"),
                         "SOUS_CATEGORIE_CINEMA_ET_AUDIOVISUEL": festival.get("sous_categorie_cinema_et_audiovisuel"),
                         "SOUS_CATEGORIE_ARTS_VISUELS_ET_ARTS_NUMERIQUES": festival.get("sous_categorie_arts_visuels_et_arts_numeriques"),
                         "SOUS_CATEGORIE_LIVRE_ET_LITTERATURE": festival.get("sous_categorie_livre_et_litterature"),
        }

        # Construction du dictionnaire final avec TOUTES les données
        metadata = {
            "DONNEES GENERALES": {
                "IDENTIFIANT": festival.get("identifiant"),
                "TITRE": festival.get("nom_du_festival"),
                "ENVERGURE_TERRITORIALE": festival.get("envergure_territoriale"),
                "REGION": festival.get("region_principale_de_deroulement"),
                "DEPARTEMENT": festival.get("departement_principal_de_deroulement"),
                "COMMUNE": festival.get("showurl"),
                "CODE_POSTAL": festival.get("code_postal_de_la_commune_principale_de_deroulement"),
                "CODES_POSTAUX_COMPLEMENTAIRES": codes_postaux,
                "NUMERO_VOIE": festival.get("numero_de_voie"),
                "TYPE_VOIE": festival.get("type_de_voie_rue_avenue_boulevard_etc"),
                "NOM_VOIE": festival.get("nom_de_la_voie"),
                "ADRESSE": adresse_complete,
                "SITE_INTERNET": festival.get("site_internet_du_festival"),
                "ANNEE_CREATION": festival.get("annee_de_creation_du_festival"),
                "DISCIPLINE_DOMINANTE": festival.get("discipline_dominante"),
                "PERIODE_PRINCIPALE_DE_ROULEMENT_DU_FESTIVAL": festival.get("periode_principale_de_deroulement_du_festival"),
                "GEOCODAGE_XY": festival.get("geocodage_xy")
            },
            "SOUS_CATEGORIES": sous_categories,
        }

        # Création du dossier : Festivals / Dept / Date
        chemin_dossier = os.path.join(DOSSIER_PRINCIPAL, departement, annee_festival)
        os.makedirs(chemin_dossier, exist_ok=True)

        # Sauvegarde
        chemin_fichier = os.path.join(chemin_dossier, f"{titre}.json")
        with open(chemin_fichier, "w", encoding="utf-8") as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)

    except Exception as e:
        print(f"❌ Erreur lors de l'écriture de {titre} : {e}")

print(f"✨ Opération terminée avec succès.")

