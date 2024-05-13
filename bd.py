from flask import Flask
from pymongo import MongoClient

def connect_database():
    info = {
        "username": "alvar",
        "password": "1234",
        "cluster": "cluster0.bvyon6w.mongodb.net",
        "database": "contaminacion"
    }
    
    url = "mongodb+srv://{username}:{password}@{cluster}/{database}?retryWrites=true&w=majority".format(**info)
    
    client = MongoClient(url)

    db = client[info["database"]]

    return db

def connect_databaseV2():
    #Conexion de la BD con Cristian GG
    info = {
        "username": "reifa",
        "password": "rafa",
        "cluster": "cluster0.bvyon6w.mongodb.net",
        "database": "contaminacion"
    }
    
    url = "mongodb+srv://{username}:{password}@{cluster}/{database}?retryWrites=true&w=majority".format(**info)
    
    # Conecta a MongoDB
    client = MongoClient(url)

    # Selecciona la base de datos
    db = client[info["database"]]
    
    return db

def search_result(info):
    db = connect_database()

    documentos = db.contaminantes.find()
    
    for doc in documentos:
        print(doc)
        return doc


search_result(connect_databaseV2())
