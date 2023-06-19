# importing pandas as pd
import pandas as pd
import csv
import glob
import datetime

def inventaire(date, produits):
    inventaire_ini = []
    inventaire_fin = []

    list = glob.glob('Inventaires/*.xlsx')
    fichiers = []
    for l in list:
        fichier = datetime.datetime.strptime(l[12:16], '%m%y')
        ini = date
        fin = date

        if(date.day == 1):
            ini = ini - datetime.timedelta(days=1)
            ini = ini.replace(day=1)

            if(fin == fichier or ini == fichier):
                fichiers.append(l)
        else:
            ini = ini.replace(day=1)
            ini = ini - datetime.timedelta(days=1)
            ini = ini.replace(day=1)
            if (fichier == ini):
                fichiers.append(l)




    for f in fichiers:
        fichier = datetime.datetime.strptime(f[12:16], '%m%y')
        read_file = pd.read_excel(f)
        read_file.to_csv("Inventaires/csv/" + f[12:16] + ".csv",
                         index=None)

        with open("Inventaires/csv/" + f[12:16] + ".csv") as file_name:
            reader = csv.reader(file_name, delimiter=',')
            for row in reader:
                if(produits.find_one({'référence': row[1]})):
                    if(row[5] == ""):
                        row[5] = 0
                    if(fin == fichier):
                        inventaire_fin.append([row[1],row[5]])
                    else:
                        inventaire_ini.append([row[1], row[5]])


    return inventaire_ini,inventaire_fin

