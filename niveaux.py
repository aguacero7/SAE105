
import pandas as pd
import zipfile 

def niveau0(path):
    
        # Ouvrir le fichier ZIP en mode lecture
    if ".zip/" in path:
        zip_file_path=path.split(".zip/")[0]
        csv_file_name=path.split(".zip/")[1]
        with zipfile.ZipFile(zip_file_path+".zip", 'r') as zip_file:

            # Lire le fichier CSV à partir du fichier ZIP

            csv_file = zip_file.open(csv_file_name)

            # Lire le fichier CSV en utilisant pandas
            df = pd.read_csv(csv_file, on_bad_lines='skip')

    else:

        df = pd.read_csv(path, on_bad_lines='skip')

    # Calculer le pourcentage de lignes à supprimer

    nb_rows_to_drop = len(df) // 100

    # Supprimer les lignes incorrectement formatées

    df.dropna(thresh=len(df) - nb_rows_to_drop, inplace=True)
    return df

niveau0("/home/pnv_lga/Téléchargements/SAE15/docs/medocs_mouvements.zip/mvtpdt.csv")