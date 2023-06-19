import csv
import pandas as pd
from pymongo  import MongoClient
import json
import os

def created_db():
    read_file = pd.read_excel("db/dbfile.xlsx")

    read_file.to_csv("db/dbfile.csv",
                    index=None,
                    line_terminator=None
                     )

    with open("db/dbfile.csv") as file_name:
        row_count = sum(1 for line in file_name)
    with open("db/dbfile.csv") as file_name:
        reader = csv.reader(file_name, delimiter=',')
        counter = 0
        with open("db/db.json", "w") as db_file:

            db_file.write("[\n")

            for row in reader:
                counter = counter + 1
                db_file.write("     {\n"
                              "         \"référence\": \"" + row[0] + "\",\n"
                              "         \"nom_du_produit\": \"" + row[1] + "\",\n"
                              "         \"prix_par_unité\": " + row[2] + ",\n"  
                              "         \"quantité_par_unité\": " + row[3] + ",\n"
                              "         \"plat\": [\n"
                              )
                i = 4

                while(i < len(row)):
                    if(row[i] != ""):
                        db_file.write("             {\"nom_du_plat\": \"" + row[i] + "\",\"quantite\": " + row[i+1][0:4] + "}")
                    i = i + 2
                    if(i < len(row)):
                        if (row[i] != ""):
                            db_file.write(",\n")
                db_file.write("\n        ]\n     }")
                if(row_count > counter):
                    db_file.write(",\n")
            db_file.write("\n]")







    #client = MongoClient("laboucheriesalon-shard-00-02.624cu.mongodb.net:27017")
    client = MongoClient("localhost:27017")

    db = client.Gestion_des_stocks
    produits = db.Produits
    produits.drop()
    produits = db.Produits

    with open('db/db.json') as f:
        file_data = json.load(f)
    produits.insert_many(file_data)

    client.close()