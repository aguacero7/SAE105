import customtkinter as ctk
from tkinter import filedialog
from CTkMessagebox import CTkMessagebox
import pandas as pd
import zipfile
from CTkListbox import *

#fonction qui vérifie que le fichier est valide
def verif_file(path):
    if path[-4:]==".csv":
        return True
    else:

        return False

def select_file():                              #fonction pr choisir un fichier
    file_path = filedialog.askopenfilename()    #on demande à l'utilisateur de choisir un fichier et on stocke le chemin ds une variabke
    if(verif_file(file_path)==False):
        CTkMessagebox(title="Erreur", message="Erreur d'extension, pensez à choisir un fichier .csv", icon="cancel")   #message d'alerte si le fichier n'est pas csv
    else:
        accueil_entry.delete(0, ctk.END)            #on supprime le texte quil ya dans le champ en dessous
        accueil_entry.insert(0, file_path)          #on le remplace par le chemin



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
        
        # Créer une listbox pour afficher la liste des fichiers CSV
        listbox = CTkListbox(top)
        listbox.pack(padx=20, pady=20, fill=ctk.BOTH, expand=True)
        
        # Ajouter les fichiers CSV à la listbox
        for file in csv_files:
            listbox.insert(ctk.END, file)
        
        # Fonction pour sélectionner un fichier CSV et l'ajouter dans accueil_entry
        def select_csv(event):
            selected_item = listbox.curselection()
            selected_file = listbox.get(selected_item)
            accueil_entry.delete(0, ctk.END)
            accueil_entry.insert(0, selected_file)
            top.destroy()
        
        # Ajouter un événement pour sélectionner un fichier CSV
        listbox.bind("<<ListboxSelect>>", select_csv)
        
        # Afficher le toplevel
        top.mainloop()
    else:
        CTkMessagebox(title="Erreur", message="Erreur d'extension, pensez à choisir un fichier .zip", icon="cancel")

app=ctk.CTk()                                   #constructeur
tabview = ctk.CTkTabview(app)                   #intialisation du system d'onglet
app.minsize(600,300)                            #taille minimale
tabview.pack(padx=20, pady=20)                  #centrer le tabview

tabview.add("Accueil")  # l'onglet accueil
for i in range(0,6):     #les onglets niveaux
    tabview.add("Niveau"+str(i))

button_1 = ctk.CTkButton(tabview.tab("Accueil"),text="Choisissez un fichier",command=open_zip)
button_1.grid(row=0,column=0,pady=(30,10))
accueil_entry = ctk.CTkEntry(tabview.tab("Accueil"), width=500)
accueil_entry.grid(row=1,column=0,pady=(30,10))

app.grid_columnconfigure(0,weight=1,)
app.mainloop()