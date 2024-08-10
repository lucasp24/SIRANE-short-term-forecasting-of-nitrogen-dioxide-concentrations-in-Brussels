import subprocess
import os
from datetime import datetime, timedelta
import shutil

# Fonction pour exécuter une simulation avec les dates spécifiées
def run_simulation(start_date, end_date, output_dir, fond_file):
    # Lecture du nom du répertoire d'écriture des résultats à partir du fichier Donnees.dat
    with open("INPUT/Donnees.dat", "r") as f:
        for line in f:
            if line.startswith("Repertoire d'ecriture des resultats"):
                result_dir = line.split("=")[1].strip()
                break
    
    # Création du chemin complet du répertoire de sortie unique
    unique_output_dir = os.path.join(output_dir, result_dir)

    # Création du nom de dossier pour cette simulation
    simulation_dir_name = start_date.strftime("%Y-%m-%d_%H-%M-%S")

    # Chemin complet du répertoire de simulation
    simulation_dir = os.path.join(unique_output_dir, simulation_dir_name)

    # Commande pour lancer la simulation avec les dates mises à jour
    command = f"./sirane-rev155-Linux64-UCLouvain-2024 INPUT/Donnees.dat Testauto2022.txt"

    # Exécution de la commande
    subprocess.run(command, shell=True)

    # Déplacement des résultats dans le dossier de sortie unique
    move_results(simulation_dir)

# Fonction pour déplacer les résultats vers le dossier de sortie
def move_results(simulation_dir):
    # Créer le dossier de simulation s'il n'existe pas déjà
    os.makedirs(simulation_dir, exist_ok=True)
    
    # Parcourir les fichiers et sous-dossiers du dossier "test"
    for root, dirs, files in os.walk("testauto"):
        # Pour chaque fichier trouvé
        for file in files:
            # Déplacer le fichier vers le dossier de simulation
            shutil.move(os.path.join(root, file), simulation_dir)

# Fonction pour mettre à jour les dates dans le fichier Donnees.dat
def update_don_dat(start_date, end_date, fond_file):
    with open("INPUT/Donnees.dat", "r") as f:
        lines = f.readlines()

    # Modifier les lignes contenant les dates de début et de fin
    for i, line in enumerate(lines):
        if "Date de debut" in line:
            lines[i] = f"Date de debut = {start_date.strftime('%d/%m/%Y %H:%M:%S')}\n"
        elif "Date de fin" in line:
            lines[i] = f"Date de fin = {end_date.strftime('%d/%m/%Y %H:%M:%S')}\n"

        # Modifier la ligne du fichier de fond
        if "Fichier de pollution de fond" in line:
            lines[i] = f"Fichier de pollution de fond = {fond_file}\n"

    # Écrire les lignes modifiées dans le fichier Don.dat
    with open("INPUT/Donnees.dat", "w") as f:
        f.writelines(lines)

# Fonction pour exécuter les simulations périodiquement toutes les 12 heures jusqu'à la fin
def run_periodic_simulations(start_date, total_duration, output_dir):
    current_date = start_date

    # Boucle pour chaque simulation de 12 heures
    while current_date < start_date + total_duration:
        # Générer le nom du fichier de fond pour cette simulation
        fond_file = generate_fond_file_name(current_date)

        # Afficher le fichier de fond sélectionné
        print(f"Date actuelle: {current_date}, Fichier de fond sélectionné: {fond_file}")

        # Mettre à jour les dates et le fichier de fond dans le fichier Donnees.dat
        update_don_dat(current_date, current_date + timedelta(days=2), fond_file)

        # Lancer la simulation avec les dates mises à jour - durée 48h (days=2)
        run_simulation(current_date, current_date + timedelta(days=2), output_dir, fond_file)

        # Avancer la date de 12 heures pour la prochaine simulation
        current_date += timedelta(hours=12)

# Fonction pour générer le nom du fichier de fond pour une date donnée
def generate_fond_file_name(start_date):
    # Formater la date pour correspondre au format dans le nom du fichier de fond
    formatted_date = start_date.strftime('%Y-%m-%d')

    # Formater l'heure de début de la simulation pour correspondre au format dans le nom du fichier de fond
    formatted_hour = start_date.strftime('%H')

    # Générer le nom du fichier en fonction de la date et de l'heure de début de la simulation
    return f"FOND/ALL/date_{formatted_date}_levtype_pl_time_{formatted_hour}_00_00_convert.dat"


# Date de début de la simulation Y/M/D H:M (01/01/2022 à minuit) 
start_date = datetime(2022, 1, 1, 0, 0)

# Durée totale de la simulation (1 an)
total_duration = timedelta(days=365)

# Dossier de sortie pour les résultats des simulations
output_dir = "test_output"

# Exécuter les simulations périodiques toutes les 12 heures jusqu'à la fin
run_periodic_simulations(start_date, total_duration, output_dir)
