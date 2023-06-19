# importing pandas as pd
import pandas as pd
from pymongo  import MongoClient
import csv
import glob
import datetime

def achat(date):

    achats = []

    list = glob.glob('Achats/*.xlsx')
    fichiers = []
    for l in list:
        #fichier = datetime.datetime.strptime(l[25:31], '%y%m%d')
        fichier = datetime.datetime.strptime(l[7:11], '%m%y')
        if (date.month == fichier.month):
            fichiers.append(l)

    #client = MongoClient("laboucheriesalon-shard-00-02.624cu.mongodb.net:27017")
    client = MongoClient("localhost:27017")

    db = client.Gestion_des_stocks
    produits = db.Produits


    for produit in produits.find():
        ref = produit['référence']
        quantite_par_unite = produit['quantité_par_unité']
        quantite = 0
        for f in fichiers:
            read_file = pd.read_excel(f)
            read_file.to_csv("Achats/csv/" + f[7:] + ".csv",
                                 index=None)
            with open("Achats/csv/" + f[7:] + ".csv") as file_name:
                reader = csv.reader(file_name, delimiter=',')
                i = 0
                #for row in reader:
                #    if(i == 8):
                #        date_livraison = datetime.datetime.strptime(row[1], '%d/%m/%Y')
                 #       break
                #    i = i + 1
                #if(date.month == date_livraison.month):
                    #if(quantite_par_unite!= 0):
                for row in reader:
                    if(ref == row[0]):
                        #if(row[-1] != ''):
                            #quantite = quantite + float(row[-1])*quantite_par_unite
                        quantite = quantite + float(row[1])/1000
                                #break
        achats.append([ref, quantite])

    client.close()

    return achats