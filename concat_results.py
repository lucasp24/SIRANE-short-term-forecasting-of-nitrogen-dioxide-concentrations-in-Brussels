import os
import pandas as pd
from datetime import datetime

# Dossier contenant les fichiers .dat
folder_path = "/Users/lucaspetit/Documents/Mémoire/SIMULATIONS/sim_2022_1an/"

# Chemin d'accès pour enregistrer le fichier Excel
excel_path = "/Users/lucaspetit/Documents/Mémoire/SIMULATIONS/data_by_station_minuit.xlsx"
excel_path12 = "/Users/lucaspetit/Documents/Mémoire/SIMULATIONS/data_by_station_midi.xlsx"

# Liste des noms de station
stations = [
    "Recept_41B008.dat", "Recept_41N043.dat", "Recept_41REG1.dat",
    "Recept_41CHA1.dat", "Recept_41R012.dat", "Recept_41R001.dat", "Recept_41R002.dat",
    "Recept_41B001.dat", "Recept_41MEU1.dat", "Recept_41B006.dat", "Recept_41B004.dat",
    "Recept_41B011.dat"
]

# Fonction pour convertir une date au format 'dd/mm/yyyy HH:MM' en objet datetime
def convert_to_datetime(date_str):
    return datetime.strptime(date_str, '%d/%m/%Y %H:%M')



#%% MINUIT


# Créer un fichier Excel pour enregistrer les données
writer = pd.ExcelWriter(excel_path, engine='xlsxwriter')

# Boucle sur chaque station
for station in stations:
    # Créer un DataFrame vide pour la station actuelle
    data_station = pd.DataFrame(columns=['Date', 'NO2_Mes', 'NO_Mes', 'O3_Mes'])

    # Parcourir les fichiers .dat dans le dossier
    for subdir, dirs, files in os.walk(folder_path):
        if subdir.endswith("00-00-00"):
            for file in files:
                if file == station:
                    file_path = os.path.join(subdir, file)
                    # Lire le fichier .dat en tant que DataFrame
                    df = pd.read_csv(file_path, sep='\t')

                    # Convertir la colonne 'Date' en datetime
                    df['Date'] = df['Date'].apply(convert_to_datetime)

                    # Transformer les colonnes se terminant par '_Mes' en valeurs numériques
                    mes_cols = [col for col in df.columns if col.endswith('_Mes')]
                    df[mes_cols] = df[mes_cols].apply(pd.to_numeric, errors='coerce')

                    # Sélectionner les lignes spécifiques
                    df_first_24 = df.iloc[:24].copy()
                    df_last_24 = df.iloc[24:48].copy()
                    df_last_48 = df.iloc[48:].copy()

                    # Renommer les colonnes des données 24h précédentes
                    df_last_24.rename(columns={'NO': 'NO-24', 'NO2': 'NO2-24', 'O3': 'O3-24'}, inplace=True)

                    # Renommer les colonnes des données 48h précédentes
                    df_last_48.rename(columns={'NO': 'NO-48', 'NO2': 'NO2-48', 'O3': 'O3-48'}, inplace=True)

                    # Fusionner les données des deux fichiers pour les mêmes dates
                    merged_df = pd.merge(df_first_24, df_last_24, on='Date', suffixes=('', '-24'), how='outer')
                    merged_df = pd.merge(merged_df, df_last_48, on='Date', suffixes=('', '-48'), how='outer')

                    # Ajouter les données fusionnées au DataFrame global
                    data_station = pd.concat([data_station, merged_df], ignore_index=True)

    # Trier les valeurs par date
    data_station.sort_values(by='Date', inplace=True)

    # Réinitialiser l'index
    data_station.reset_index(drop=True, inplace=True)

    # Regrouper les données en utilisant la colonne 'Date' et appliquer la méthode de fusion 'first'
    data_station = data_station.groupby('Date').first().reset_index()

    # Supprimer les colonnes de date superflues
    data_station.drop(columns=['NO2_Mes-24', 'NO_Mes-24', 'O3_Mes-24', 'NO2_Mes-48', 'NO_Mes-48', 'O3_Mes-48'], inplace=True, errors='ignore')

    # Enregistrer les données de la station dans une feuille de calcul Excel
    data_station.to_excel(writer, sheet_name=station, index=False)

# Fermer le fichier Excel
writer.save()

#%% MIDI 

# Créer un fichier Excel pour enregistrer les données
writer12 = pd.ExcelWriter(excel_path12, engine='xlsxwriter')

# Boucle sur chaque station
for station in stations:
    # Créer un DataFrame vide pour la station actuelle
    data_station = pd.DataFrame(columns=['Date', 'NO2_Mes', 'NO_Mes', 'O3_Mes'])

    # Parcourir les fichiers .dat dans le dossier
    for subdir, dirs, files in os.walk(folder_path):
        if subdir.endswith("12-00-00"):
            for file in files:
                if file == station:
                    file_path = os.path.join(subdir, file)
                    # Lire le fichier .dat en tant que DataFrame
                    df = pd.read_csv(file_path, sep='\t')

                    # Convertir la colonne 'Date' en datetime
                    df['Date'] = df['Date'].apply(convert_to_datetime)

                    # Transformer les colonnes se terminant par '_Mes' en valeurs numériques
                    mes_cols = [col for col in df.columns if col.endswith('_Mes')]
                    df[mes_cols] = df[mes_cols].apply(pd.to_numeric, errors='coerce')

                    # Sélectionner les lignes spécifiques
                    df_first_24 = df.iloc[:24].copy()
                    df_last_24 = df.iloc[24:48].copy()
                    df_last_48 = df.iloc[48:].copy()

                    # Renommer les colonnes des données 24h précédentes
                    df_last_24.rename(columns={'NO': 'NO-24', 'NO2': 'NO2-24', 'O3': 'O3-24'}, inplace=True)

                    # Renommer les colonnes des données 48h précédentes
                    df_last_48.rename(columns={'NO': 'NO-48', 'NO2': 'NO2-48', 'O3': 'O3-48'}, inplace=True)

                    # Fusionner les données des deux fichiers pour les mêmes dates
                    merged_df = pd.merge(df_first_24, df_last_24, on='Date', suffixes=('', '-24'), how='outer')
                    merged_df = pd.merge(merged_df, df_last_48, on='Date', suffixes=('', '-48'), how='outer')

                    # Ajouter les données fusionnées au DataFrame global
                    data_station = pd.concat([data_station, merged_df], ignore_index=True)

    # Trier les valeurs par date
    data_station.sort_values(by='Date', inplace=True)

    # Réinitialiser l'index
    data_station.reset_index(drop=True, inplace=True)

    # Regrouper les données en utilisant la colonne 'Date' et appliquer la méthode de fusion 'first'
    data_station = data_station.groupby('Date').first().reset_index()

    # Supprimer les colonnes de date superflues
    data_station.drop(columns=['NO2_Mes-24', 'NO_Mes-24', 'O3_Mes-24', 'NO2_Mes-48', 'NO_Mes-48', 'O3_Mes-48'], inplace=True, errors='ignore')

    # Enregistrer les données de la station dans une feuille de calcul Excel
    data_station.to_excel(writer12, sheet_name=station, index=False)

# Fermer le fichier Excel
writer12.save()