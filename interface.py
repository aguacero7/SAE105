import customtkinter as ctk
from tkinter import filedialog
from CTkMessagebox import CTkMessagebox
import pandas as pd
import zipfile
from CTkListbox import *
import chardet
from CTkTable import *
from io import StringIO


def main():
    dataf=None



    def niveau0(path):
        global dataf
            # Ouvrir le fichier ZIP en mode lecture
        if ".zip/" in path:
            zip_file_path=path.split(".zip/")[0]
            csv_file_name=path.split(".zip/")[1]
            with zipfile.ZipFile(zip_file_path + ".zip", 'r') as zip_file:

                #Lire le csv du zip

                csv_file = zip_file.open(csv_file_name)

                rawdata = csv_file.read()

                encoding = chardet.detect(rawdata)['encoding']
                # mettre le csv dans une dataframe

                df = pd.read_csv(StringIO(rawdata.decode(encoding)), sep=";", on_bad_lines='skip')


        else:
            # Détecter l'encodage du fichier CSV

            with open(path, 'rb') as f:

                rawdata = f.read()

                encoding = chardet.detect(rawdata)['encoding']
            # Lire le fichier CSV avec l'encodage détecté

            df = pd.read_csv(path, encoding=encoding,sep=";", on_bad_lines='skip')

        print(f"Encodage détecté: {encoding}")
        print(df.head())
        ctk.CTkLabel(tabview.tab("Niveau0"), text="En-têtes").grid(row=0, column=4, pady=(0, 10))
        if df is not None:

           for i, header in enumerate(df.columns.values):
                ctk.CTkLabel(tabview.tab("Niveau0"), text=header).grid(row=i+2, column=4, pady=(0, 10))

        return df

    def select_file():                              #fonction pr choisir un fichier
        file_path = filedialog.askopenfilename()    #on demande à l'utilisateur de choisir un fichier et on stocke le chemin ds une variabke
        if(file_path.endswith(".csv")):
            accueil_entry.delete(0, ctk.END)            #on supprime le texte quil ya dans le champ en dessous
            accueil_entry.insert(0, file_path)          #on le remplace par le chemin
        else:
            CTkMessagebox(title="Erreur", message="Erreur d'extension, pensez à choisir un fichier .csv", icon="cancel")   #message d'alerte si le fichier n'est pas csv





    def open_zip():
        # Demander à l'utilisateur de choisir un fichier ZIP
        zip_path = filedialog.askopenfilename(filetypes=[("Fichiers ZIP", "*.zip")])
        
        # Vérifier si le fichier est valide
        if zip_path.endswith(".zip"):
            # Extraire les fichiers CSV du ZIP
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                files = zip_ref.namelist()
                csv_files = [file for file in files if file.endswith(".csv")]
            
            # Créer un nouveau toplevel pour afficher la liste des fichiers CSV
            top = ctk.CTkToplevel(app)
            top.title("Fichiers dans le zip")
            
            # Creer une listbox pour afficher la liste des fichiers CSV
            listbox = CTkListbox(top)
            listbox.pack(padx=20, pady=20, fill=ctk.BOTH, expand=True)
            
            # Ajouter les fichiers CSV à la listbox
            for file in csv_files:
                listbox.insert(ctk.END, file)

            # sélectionner un fichier CSV et l'ajouter dans accueil_entry
            def select_csv(event):
                selected_item = listbox.curselection()
                selected_file = listbox.get(selected_item)

                accueil_entry.delete(0, ctk.END)
                path=zip_path+"/"+selected_file         #ajouter le chemin du zip et le fichier ensemble
                accueil_entry.insert(0, path)


                top.destroy()
            
            # jouter un événement pour sélectionner un fichier CSV
            listbox.bind("<<ListboxSelect>>", select_csv)
            
            # Afficher le toplevel
            top.mainloop()
        else:
            CTkMessagebox(title="Erreur", message="Erreur d'extension, pensez à choisir un fichier .zip", icon="cancel")

    


    app=ctk.CTk()                                   #constructeur
    app.minsize(600,300)                            #taille minimale



    ########-----------tabview------------#########
    tabview = ctk.CTkTabview(app)                   #intialisation du system d'onglet
    tabview.pack(padx=20, pady=20)                  #centrer le tabview
    tabview.add("Accueil")  # l'onglet accueil
    for i in range(0,6):     #les onglets niveaux
        tabview.add("Niveau"+str(i))
    


    ########-----------accueil------------#########
    button_1 = ctk.CTkButton(tabview.tab("Accueil"),text="Choisissez un ZIP",command=open_zip)

    button_2 = ctk.CTkButton(tabview.tab("Accueil"),text="Choisissez un fichier",command=select_file)

    accueil_entry = ctk.CTkEntry(tabview.tab("Accueil"), width=500)


    button_1.grid(row=0,column=1,pady=(30,10))

    button_2.grid(row=0,column=3,pady=(30,10))

    accueil_entry.grid(row=1,column=1,columnspan=3,pady=(30,10))


    ########-----------Niveau 0------------#########
    button_01 = ctk.CTkButton(tabview.tab("Niveau0"), text="Lire le CSV",command=lambda: niveau0(accueil_entry.get()))
    button_01.grid(row=0, column=1, pady=(30,10))

    app.grid_columnconfigure(0,weight=10)
    app.mainloop()



if __name__ == "__main__":
    main()