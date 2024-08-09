{\rtf1\ansi\ansicpg1252\cocoartf2639
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww15280\viewh10160\viewkind0
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import subprocess\
import os\
from datetime import datetime, timedelta\
import shutil\
\
# Fonction pour ex\'e9cuter une simulation avec les dates sp\'e9cifi\'e9es\
def run_simulation(start_date, end_date, output_dir, fond_file):\
    # Lecture du nom du r\'e9pertoire d'\'e9criture des r\'e9sultats \'e0 partir du fichier Don.dat\
    with open("INPUT/Donnees.dat", "r") as f:\
        for line in f:\
            if line.startswith("Repertoire d'ecriture des resultats"):\
                result_dir = line.split("=")[1].strip()\
                break\
    \
    # Cr\'e9ation du chemin complet du r\'e9pertoire de sortie unique\
    unique_output_dir = os.path.join(output_dir, result_dir)\
\
    # Cr\'e9ation du nom de dossier pour cette simulation\
    simulation_dir_name = start_date.strftime("%Y-%m-%d_%H-%M-%S")\
\
    # Chemin complet du r\'e9pertoire de simulation\
    simulation_dir = os.path.join(unique_output_dir, simulation_dir_name)\
\
    # Commande pour lancer la simulation avec les dates mises \'e0 jour\
    command = f"./sirane-rev155-Linux64-UCLouvain-2024 INPUT/Donnees.dat Testauto2022juil_dec_meteomes.txt"\
\
    # Ex\'e9cution de la commande\
    subprocess.run(command, shell=True)\
\
    # D\'e9placement des r\'e9sultats dans le dossier de sortie unique\
    move_results(simulation_dir)\
\
# Fonction pour d\'e9placer les r\'e9sultats vers le dossier de sortie\
def move_results(simulation_dir):\
    # Cr\'e9er le dossier de simulation s'il n'existe pas d\'e9j\'e0\
    os.makedirs(simulation_dir, exist_ok=True)\
    \
    # Parcourir les fichiers et sous-dossiers du dossier "test"\
    for root, dirs, files in os.walk("testauto_meteomes"):\
        # Pour chaque fichier trouv\'e9\
        for file in files:\
            # D\'e9placer le fichier vers le dossier de simulation\
            shutil.move(os.path.join(root, file), simulation_dir)\
\
# Fonction pour mettre \'e0 jour les dates dans le fichier Don.dat\
def update_don_dat(start_date, end_date, fond_file):\
    with open("INPUT/Donnees.dat", "r") as f:\
        lines = f.readlines()\
\
    # Modifier les lignes contenant les dates de d\'e9but et de fin\
    for i, line in enumerate(lines):\
        if "Date de debut" in line:\
            lines[i] = f"Date de debut = \{start_date.strftime('%d/%m/%Y %H:%M:%S')\}\\n"\
        elif "Date de fin" in line:\
            lines[i] = f"Date de fin = \{end_date.strftime('%d/%m/%Y %H:%M:%S')\}\\n"\
\
        # Modifier la ligne du fichier de fond\
        if "Fichier de pollution de fond" in line:\
            lines[i] = f"Fichier de pollution de fond = \{fond_file\}\\n"\
\
    # \'c9crire les lignes modifi\'e9es dans le fichier Don.dat\
    with open("INPUT/Donnees.dat", "w") as f:\
        f.writelines(lines)\
\
# Fonction pour ex\'e9cuter les simulations p\'e9riodiquement toutes les 12 heures jusqu'\'e0 la fin\
def run_periodic_simulations(start_date, total_duration, output_dir):\
    current_date = start_date\
\
    # Boucle pour chaque simulation de 12 heures\
    while current_date < start_date + total_duration:\
        # G\'e9n\'e9rer le nom du fichier de fond pour cette simulation\
        fond_file = generate_fond_file_name(current_date)\
\
        # Afficher le fichier de fond s\'e9lectionn\'e9\
        print(f"Date actuelle: \{current_date\}, Fichier de fond s\'e9lectionn\'e9: \{fond_file\}")\
\
        # Mettre \'e0 jour les dates et le fichier de fond dans le fichier Don.dat\
        update_don_dat(current_date, current_date + timedelta(days=2), fond_file)\
\
        # Lancer la simulation avec les dates mises \'e0 jour\
        run_simulation(current_date, current_date + timedelta(days=2), output_dir, fond_file)\
\
        # Avancer la date de 12 heures pour la prochaine simulation\
        current_date += timedelta(hours=12)\
\
# Fonction pour g\'e9n\'e9rer le nom du fichier de fond pour une date donn\'e9e\
def generate_fond_file_name(start_date):\
    # Formater la date pour correspondre au format dans le nom du fichier de fond\
    formatted_date = start_date.strftime('%Y-%m-%d')\
\
    # Formater l'heure de d\'e9but de la simulation pour correspondre au format dans le nom du fichier de fond\
    formatted_hour = start_date.strftime('%H')\
\
    # G\'e9n\'e9rer le nom du fichier en fonction de la date et de l'heure de d\'e9but de la simulation\
    return f"FOND/ALL/date_\{formatted_date\}_levtype_pl_time_\{formatted_hour\}_00_00_convert.dat"\
\
\
# Date de d\'e9but de la simulation (\'e0 midi)\
start_date = datetime(2022, 11, 25, 0, 0)\
\
# Dur\'e9e totale de la simulation\
total_duration = timedelta(days=1)\
\
# Dossier de sortie pour les r\'e9sultats des simulations\
output_dir = "test_output_juil_dec_meteomes"\
\
# Ex\'e9cuter les simulations p\'e9riodiques toutes les 12 heures jusqu'\'e0 la fin\
run_periodic_simulations(start_date, total_duration, output_dir)\
}