import customtkinter as ctk
from tkinter import filedialog
from CTkMessagebox import CTkMessagebox
import pandas as pd
import zipfile
from CTkListbox import *
import chardet
from CTkTable import *
from io import StringIO
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def main():
    dataf = None
    def level5(df, ax,frame):
        df_grouped = df.groupby('MAGASIN')['TYPEMVT'].value_counts(normalize=True)
        df_grouped = df_grouped.mul(100).round(1)
        df_grouped.unstack().plot(kind='bar', stacked=True, ax=ax)
        ax.set_title('Répartition des types de mouvements par magasin')
        ax.set_xlabel('Magasin')
        ax.set_ylabel('Pourcentage (%)')

    def level4(df, frame):
        années = ["2021","2022","2023"]
        value = [0.0,0.0,0.0]
        for i in df.itertuples():
            if i.DATEMVT[-4:] != '2020':
                r = années.index(i.DATEMVT[-4:])
                h = i.VALHT
                if "," in h:
                    z = h.split(",")
                    if len(z) == 2:
                        h = z[0] + "." + z[1]
                    else:
                        h = z[0]
                value[r] += float(h)
        print(value)
        fig, ax = plt.subplots()  # Creer la figure
        ax.pie(value, labels=années, autopct="%1.1f%%")
        ax.set_title("Proportion de valeurs par année")

        
        canvas = FigureCanvasTkAgg(fig, master=frame)  
        canvas.draw()                                  
        canvas.get_tk_widget().grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)

    def level3(df,frame):
        mois = [["janvier","01"],["fevrier","02"],["mars","03"],["avril","04"],["mai","05"],["juin","06"],["juillet","07"],["aout","08"],["septembre","09"],["octobre","10"],["novembre","11"],["decembre","12"]]
        mois = []
        nbmvt = []
        for x in df.itertuples():
            v = x.DATEMVT[3:]
            if v in mois:
                i = mois.index(v)
                nbmvt[i] += 1
            else :
                mois.append(v)
                nbmvt.append(1)
        for i in mois:
            t = i.split("/")
            for j in mois:
                if j[1] == t[0]:
                    g = mois.index(i)
                    mois[g] = j[0] + "\n" + t[1]
                    print(mois[g])

        fig, ax = plt.subplots()  
        ax.bar(mois, nbmvt)
        ax.set_title("Nombre de mouvements / mois")
        ax.set_xlabel("mois")

        ax.set_xticks(range(len(mois)))
        ax.set_xticklabels([mois[i // 5] for i in range(len(mois))])
        canvas = FigureCanvasTkAgg(fig, master=frame)  
        canvas.draw()                                  
        canvas.get_tk_widget().pack(side="top", fill="both", expand=True)  

        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)

    def level1(df,frame):
        years = []
        value = []
        for i in df.itertuples():
            z = i.DATEMVT[-4:]
            if z in years:
                r = years.index(z)
                value[r] += 1
            else:
                years.append(z)
                value.append(1)
        fig, ax = plt.subplots()  
        ax.bar(years, value)
        ax.set_title("Nombre de mouvements par année")
        ax.set_xlabel("Années")

        canvas = FigureCanvasTkAgg(fig, master=frame)  
        canvas.draw()                                  
        canvas.get_tk_widget().pack(side="top", fill="both", expand=True)  

        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)
    def level0(path):
        global dataf
        # Ouvrir le fichier ZIP en mode lecture
        if ".zip/" in path:
            zip_file_path = path.split(".zip/")[0]
            csv_file_name = path.split(".zip/")[1]
            with zipfile.ZipFile(zip_file_path + ".zip", 'r') as zip_file:

                # Lire le csv du zip

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

            df = pd.read_csv(path, encoding=encoding, sep=";", on_bad_lines='skip')

        print(f"Encodage détecté: {encoding}")
        print(df.head())
        ctk.CTkLabel(tabview.tab("Niveau0"), text="En-têtes").grid(row=0, column=4, pady=(0, 10))
        if df is not None:

            for i, header in enumerate(df.columns.values):
                ctk.CTkLabel(tabview.tab("Niveau0"), text=header).grid(row=i + 2, column=4, pady=(0, 10))
        level1(df,niveau1_frame)
        level3(df,niveau3_frame)
        level4(df,niveau4_frame)
        figure5 = plt.Figure(figsize=(10, 5))
        niveau5_frame.canvas = FigureCanvasTkAgg(figure5, master=niveau5_frame)
        niveau5_ax = figure5.add_subplot(111)
        niveau5_frame.canvas.get_tk_widget().grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
        return df

    def select_file():  # fonction pr choisir un fichier
        file_path = filedialog.askopenfilename()  # on demande à l'utilisateur de choisir un fichier et on stocke le chemin ds une variabke
        if (file_path.endswith(".csv")):
            accueil_entry.delete(0, ctk.END)  # on supprime le texte quil ya dans le champ en dessous
            accueil_entry.insert(0, file_path)  # on le remplace par le chemin
        else:
            CTkMessagebox(title="Erreur", message="Erreur d'extension, pensez à choisir un fichier .csv",
                          icon="cancel")  # message d'alerte si le fichier n'est pas csv

    def open_zip():
        # Demander à l'utilisateur de choisir un fichier ZIP
        zip_path = filedialog.askopenfilename(filetypes=[("Fichiers ZIP", "*.zip")])

        # Vérifier si le fichier est valide
        if zip_path.endswith(".zip"):
            # Extraire les fichiers CSV du ZIP
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                files = zip_ref.namelist()
                csv_files = [file for file in files if file.endswith(".csv")]

            # Créer un nouveau toplevel
            top = ctk.CTkToplevel(app)
            top.title("Fichiers dans le zip")

            # liste des fichiers CSV
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
                path = zip_path + "/" + selected_file  # ajouter le chemin du zip et le fichier ensemble
                accueil_entry.insert(0, path)

                top.destroy()

            # jouter un événement pour sélectionner un fichier CSV
            listbox.bind("<<ListboxSelect>>", select_csv)

            # Afficher le toplevel
            top.mainloop()
        else:
            CTkMessagebox(title="Erreur", message="Erreur d'extension, pensez à choisir un fichier .zip", icon="cancel")


    app = ctk.CTk()  # constructeur
    app.minsize(600, 300)  # taille minimale

    ########-----------tabview------------#########
    tabview = ctk.CTkTabview(app)  # intialisation du system d'onglet
    tabview.pack(padx=20, pady=20)  # centrer le tabview
    tabview.add("Accueil")  # l'onglet accueil
    for i in range(0, 6):  # les onglets niveaux
        tabview.add("Niveau" + str(i))

    ########-----------accueil------------#########
    button_1 = ctk.CTkButton(tabview.tab("Accueil"), text="Choisissez un ZIP", command=open_zip)

    button_2 = ctk.CTkButton(tabview.tab("Accueil"), text="Choisissez un fichier", command=select_file)

    accueil_entry = ctk.CTkEntry(tabview.tab("Accueil"), width=500)
    

    button_1.grid(row=0, column=1, pady=(30, 10))

    button_2.grid(row=0, column=3, pady=(30, 10))

    accueil_entry.grid(row=1, column=1, columnspan=3, pady=(30, 10))

    ########-----------Niveau 0------------#########
    button_01 = ctk.CTkButton(tabview.tab("Niveau0"), text="Lire le CSV", command=lambda: level0(accueil_entry.get()))
    button_01.grid(row=0, column=1, pady=(30, 10))


########-----------Niveau 1------------#########
    niveau1_frame = ctk.CTkFrame(tabview.tab("Niveau1"))  
    niveau1_frame.grid(row=0, column=0, sticky="nsew")
########-----------Niveau 3------------#########
    niveau3_frame = ctk.CTkFrame(tabview.tab("Niveau3")) 
    niveau3_frame.grid(row=0, column=0, sticky="nsew")
########-----------Niveau 4------------#########
    niveau4_frame = ctk.CTkFrame(tabview.tab("Niveau4")) 
    niveau4_frame.grid(row=0, column=0, sticky="nsew")
########-----------Niveau 5------------#########
    niveau5_frame = ctk.CTkFrame(tabview.tab("Niveau5")) 
    niveau5_frame.grid(row=0, column=0, sticky="nsew")

    app.grid_columnconfigure(0, weight=10)
    app.mainloop()


if __name__ == "__main__":
    main()
