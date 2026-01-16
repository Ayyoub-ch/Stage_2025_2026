import os
import time

# Dossier où sont tous tes scripts
SCRIPTS_DIR = "."  # à adapter si nécessaire

# Vérifier si le dossier existe AVANT de lancer les scripts
if not os.path.exists(SCRIPTS_DIR):
    print(f"Erreur : le dossier {SCRIPTS_DIR} n'existe pas !")
    exit(1)

# Liste des scripts à exécuter (avec chemin relatif)
scripts = [
    "area.py",
    "zones.py",
    "compet_all.py",
    "compet_existante.py",
    "compet_standing.py",
    "match_actuel.py",
    "match_a_venir.py",
    "team.py",
]

# Boucle sur chaque script
for script in scripts:
    print(f"\n=== Exécution de {script} ===\n")
    os.system(f"python {os.path.join(SCRIPTS_DIR, script)}")
    print(f"\n=== Fin de {script}, pause 10s ===\n")
    time.sleep(10)
print("Tous les scripts ont été exécutés.")
