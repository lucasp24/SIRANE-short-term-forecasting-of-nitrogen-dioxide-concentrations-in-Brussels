import pandas as pd

# Chemin vers le fichier Excel
excel_path = "/Users/.../data_by_station_minuit.xlsx"
excel_path12 = "/Users/.../data_by_station_midi.xlsx"

# Définition des noms de colonnes
columns = [
    'Date',
    'NO2_Mes', 'NO_Mes', 'O3_Mes',
    'NO2_Mod', 'NO_Mod', 'O3_Mod',
    'NO2_Mod-12', 'NO_Mod-12', 'O3_Mod-12',
    'NO2_Mod-24', 'NO_Mod-24', 'O3_Mod-24',
    'NO2_Mod-36', 'NO_Mod-36', 'O3_Mod-36',
    'NO2_Mod-48', 'NO_Mod-48', 'O3_Mod-48'
]

# Stations
stations = [
    "Recept_41B008.dat", "Recept_41N043.dat", "Recept_41REG1.dat",
    "Recept_41CHA1.dat", "Recept_41R012.dat", "Recept_41R001.dat", "Recept_41R002.dat",
    "Recept_41B001.dat", "Recept_41MEU1.dat", "Recept_41B006.dat", "Recept_41B004.dat",
    "Recept_41B011.dat"
]

# Charger les données pour chaque station
dataframes = {}
for station in stations:
    # Lire les données pour la station depuis le fichier Excel
    data_station = pd.read_excel(excel_path, sheet_name=station)
    data_station_12 = pd.read_excel(excel_path12, sheet_name=station)
    
    if not data_station.empty and not data_station_12.empty:

        # Création du DataFrame avec les colonnes définies et les données copiées
        df = pd.DataFrame(columns=columns)
        
        # Copie des valeurs des quatre premières colonnes du fichier Excel dans les quatre premières colonnes du DataFrame
        df[columns[:4]] = data_station.iloc[:, :4]
        
        df.iloc[0:12, 4:7] = data_station.iloc[:12, 4:7]
        df.iloc[12:24, 7:10] = data_station.iloc[12:24, 4:7]
        df.iloc[24:36, 10:13] = data_station.iloc[24:36, 7:10]
        df.iloc[36:48, 13:16] = data_station.iloc[36:48, 7:10]


        df.iloc[24:36, 4:7] = data_station.iloc[24:36, 4:7]
        df.iloc[36:48, 7:10] = data_station.iloc[36:48, 4:7]
        
        
        
        df.iloc[12:24, 4:7] = data_station_12.iloc[:12, 4:7]
        df.iloc[24:36, 7:10] = data_station_12.iloc[12:24, 4:7]
        df.iloc[36:48, 4:7] = data_station_12.iloc[24:36, 4:7]
        df.iloc[36:48, 10:13] = data_station_12.iloc[24:36, 7:10]
        
        
        df.iloc[:, 1:] = df.iloc[:, 1:].apply(pd.to_numeric, errors='coerce')

        # Boucle qui copie/colle les valeurs pour chaque horizon
        try:
            for i in range(48, len(df), 48):
                df.iloc[i:i+12, 10:13] = data_station.iloc[i:i+12, 7:10]  
                df.iloc[i+12:i+24, 13:16] = data_station.iloc[i+12:i+24, 7:10] 
                df.iloc[i:i+1, 16:19] = data_station.iloc[i:i+1, 10:13]   
                df.iloc[i+24:i+25, 16:19] = data_station.iloc[i+24:i+25, 10:13]   
                df.iloc[i:i+12, 4:7] = data_station.iloc[i:i+12, 4:7]   
                df.iloc[i+12:i+24, 7:10] = data_station.iloc[i+12:i+24, 4:7]   
                df.iloc[i+24:i+36, 10:13] = data_station.iloc[i+24:i+36, 7:10]   
                df.iloc[i+36:i+48, 13:16] = data_station.iloc[i+36:i+48, 7:10]  
                df.iloc[i+24:i+36, 4:7] = data_station.iloc[i+24:i+36, 4:7]   
                df.iloc[i+36:i+48, 7:10] = data_station.iloc[i+36:i+48, 4:7] 

                df.iloc[i+12:i+24, 4:7] = data_station_12.iloc[i:i+12, 4:7]  
                df.iloc[i:i+12, 13:16] = data_station_12.iloc[i-12:i, 7:10]  
                df.iloc[i+24:i+36, 13:16] = data_station_12.iloc[i+12:i+24, 7:10] 
                df.iloc[i+12:i+24, 10:13] = data_station_12.iloc[i:i+12, 7:10]   
                df.iloc[i:i+12, 7:10] = data_station_12.iloc[i-12:i, 4:7]   
                df.iloc[i+24:i+36, 7:10] = data_station_12.iloc[i+12:i+24, 4:7]   
                df.iloc[i+36:i+48, 4:7] = data_station_12.iloc[i+24:i+36, 4:7]   
                df.iloc[i+36:i+48, 10:13] = data_station_12.iloc[i+24:i+36, 7:10]   
        except ValueError:
            pass  # Ignorer l'erreur ValueError

        dataframes[station] = df
    

# Chemin de sauvegarde du fichier Excel contenant toutes les feuilles
output_excel_path = "/Users/.../data_by_station_combined.xlsx"

# Création d'un writer Excel
writer = pd.ExcelWriter(output_excel_path, engine='xlsxwriter')

# Pour chaque station et son DataFrame correspondant dans le dictionnaire
for station, df in dataframes.items():
    # Écriture du DataFrame dans une feuille Excel portant le nom de la station
    df.to_excel(writer, sheet_name=station, index=False)

# Sauvegarde du fichier Excel
writer.save()

    

    
        



