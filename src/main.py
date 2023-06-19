import ventes
import inventaire
import achat
import pandas as pd
from pymongo import MongoClient
import db.createdb as db

db.created_db()

#client = MongoClient("laboucheriesalon-shard-00-02.624cu.mongodb.net:27017")
client = MongoClient("localhost:27017")

db = client.Gestion_des_stocks
produits = db.Produits

ventes, date = ventes.ventes()

inventaire_ini,inventaire_fin = inventaire.inventaire(date, produits)

achats = achat.achat(date)

inventaire_ini.sort(key=lambda produit: produit[0])
inventaire_fin.sort(key=lambda produit: produit[0])
ventes.sort(key=lambda produit: produit[0])
achats.sort(key=lambda produit: produit[0])

print(date)
inventaire_the = []
for i in range(len(ventes)):
    inventaire_the.append([ventes[i][0],float(inventaire_ini[i][1]) + float(achats[i][1]) - float(ventes[i][1])])

resultat = []
if(len(inventaire_fin) == 0):
    resultat.append("")
    resultat.append(inventaire_the,)

else:
    total = 0
    resultat.append(["Restaurant LaBoucherie", "", "", "","","","","",""])
    resultat.append(["","","","","","","","",""])
    resultat.append(["Écart du mois de : ", date.strftime("%B %Y"), "", "","","","","",""])
    resultat.append(["","","","","","","","",""])
    resultat.append(["","","","","","","","",""])
    resultat.append(["Référence", "Produit", "Inventaire Initial (en kg)", "Achats (en kg)", "Ventes (en kg)", "Inventaire Final (en kg)", "Écart (en kg)", "Écart (en €)","Ratio (en %)"])
    resultat_bis = []
    double = [["131071","132085"],["131072","132086"],["131106","132078"]]
    prix = [["131071","132085"],["131072","132086"],["131106","132078"]]
    length = int(len(double))
    for i in range(len(ventes)):
        produit = produits.find_one({'référence': ventes[i][0]})
        for j in range(length):
            for k in range(2):
                if(ventes[i][0] == double[j][k]):
                    double[j][k] = i
                    prix[j][k] = produit['prix_par_unité']
        resultat_bis.append([produit['référence'],produit['nom_du_produit'],inventaire_ini[i][1], achats[i][1], ventes[i][1], inventaire_fin[i][1], float(inventaire_fin[i][1]) - float(inventaire_the[i][1]), (float(inventaire_fin[i][1]) - float(inventaire_the[i][1])) * produit['prix_par_unité'], ((float(inventaire_fin[i][1]) - float(inventaire_the[i][1]))/float(ventes[i][1]))*100])

        i = i + 1

    for j in range(length):
        a = double[j][0]
        b = double[j][1]
        a_prix = prix[j][0]
        b_prix = prix[j][1]
        res = (resultat_bis[a][6]+resultat_bis[b][6]-resultat_bis[a][4])/2
        a_vente = resultat_bis[a][6] - res
        b_vente = resultat_bis[b][6] - res
        resultat_bis[a][4] = b_vente
        resultat_bis[a][6] = res
        resultat_bis[a][7] = res * float(a_prix)
        resultat_bis[a][8] = "PR"
        resultat_bis[b][4] = a_vente
        resultat_bis[b][6] = res
        resultat_bis[b][7] = res * float(b_prix)
        resultat_bis[b][8] = "PR"

    resultat_bis.sort(key=lambda produit: produit[7])
    resultat.extend(resultat_bis)
    for i in range(len(resultat_bis)):
        total = total + resultat_bis[i][7]
    resultat.append(["","","","","","","Total",total])
with pd.ExcelWriter('résultat.xlsx',mode='w') as writer:
    dataframe = pd.DataFrame(resultat)
    dataframe.to_excel(writer, header = False, index = False, float_format="%.2f")
