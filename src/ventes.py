# import de notre Classe MongoClient
from pymongo  import MongoClient
import csv
import glob
import os
import datetime

def ventes():
    ventes = []

    #dernier fichier et avoir la date
    list_of_files = glob.glob('Ventes/*')
    latest_file = max(list_of_files, key=os.path.getctime)

    if (latest_file[11] == '-'):
        date = datetime.datetime.strptime(latest_file[7:11], '%m%y')
    else:
        date = datetime.datetime.strptime(latest_file[7:13], '%d%m%y')

    #client = MongoClient("laboucheriesalon-shard-00-02.624cu.mongodb.net:27017")
    client = MongoClient("localhost:27017")

    db = client.Gestion_des_stocks
    produits = db.Produits

    #Récupération des ventes du mois


    for produit in produits.find():
        ref = produit['référence']
        quantite_produit = 0.0

        plats = produit['plat']
        for plat in plats:
            nom_de_plat = plat['nom_du_plat']

            quantite = plat['quantite']
            var = None
            var_quantite = 0.0
            with open(latest_file, encoding="iso-8859-1") as file_name:
                file_ventes = csv.reader(file_name, delimiter=';')
                for ligne in file_ventes:
                    if (var == ligne[3]):
                        var_quantite = ligne[4]
                        if(var == "Total Brut" ):
                            break
                        else:
                            var = "Total Brut"
                    elif(var == "Total Net"):
                        break
                    elif (ligne[3] == nom_de_plat):
                        var = "Total Net"
                    else:
                        var = None
                if(type(var_quantite) == str):
                    quantite_produit = float(quantite_produit) + float(var_quantite[0:-3]) * quantite
                else:
                    quantite_produit = float(quantite_produit) + var_quantite * quantite

        ventes.append([ref,round(quantite_produit,2)])

    return ventes, date
    # affichage un objet
    client.close()