import customtkinter as ctk
from tkinter import filedialog
from CTkMessagebox import CTkMessagebox
import pandas as pd
import zipfile

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
    top = ctk.CTkToplevel(app)
    top.title("Fichiers dans le zip")
    #treeview = ctk.CTkTreeview(top)
    #treeview.pack(padx=20, pady=20)
    #with zipfile.ZipFile(path, 'r') as zip_ref:
    #    files = zip_ref.namelist()
    #for file in files:
        #treeview.insert("", "end", text=file)
    #top.mainloop()

app=ctk.CTk()                                   #constructeur
tabview = ctk.CTkTabview(app)                   #intialisation du system d'onglet
app.minsize(600,300)                            #taille minimale
tabview.pack(padx=20, pady=20)                  #

tabview.add("Accueil")  # l'onglet accueil
for i in range(0,6):     #les onglets niveaux
    tabview.add("Niveau"+str(i))

button_1 = ctk.CTkButton(tabview.tab("Accueil"),text="Choisissez un fichier",command=select_file)
button_1.grid(row=0,column=0,pady=(30,10))
accueil_entry = ctk.CTkEntry(tabview.tab("Accueil"), width=500)
accueil_entry.grid(row=1,column=0,pady=(30,10))

app.grid_columnconfigure(0,weight=1)
app.mainloop()