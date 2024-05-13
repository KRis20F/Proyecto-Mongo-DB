from pymongo import MongoClient
from pymongo.server_api import ServerApi

# def connect_database():
#     info = {
#         "username": "alvar",
#         "password": "1234",
#         "cluster": "cluster0.bvyon6w.mongodb.net",
#         "database": "contaminacion"
#     }
    
#     url = "mongodb+srv://{username}:{password}@{cluster}/{database}?retryWrites=true&w=majority".format(**info)
    
#     client = MongoClient(url)

#     db = client[info["database"]]

#     return db

def connect_databaseV2():  #Cambio de usuario si no estamos conectados
    #Conexion de la BD con Cristian GG
    uri = "mongodb+srv://reifa:rafa@contaminacion.4m05tim.mongodb.net/?retryWrites=true&w=majority&appName=contaminacion"
    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        return client["ContaminacionBCN"]
    except Exception as e:
        print(e)
        return None


connect_databaseV2()

def get_all_database():
    bd = connect_databaseV2()
    
    colecciones = ["CalidadAire" , "Contaminantes" , "Estaciones"]
    documents = []
    
    for name_doc in colecciones:
        print(f"Estas en la Coleccion {name_doc}")
        coleccion = bd[name_doc]
        for doc in coleccion.find():
            documents.append(doc)
        print()
        
    bd.close
    return documents
        
        
        
def get_data_contamination(neighborhood):
    
    documents = get_all_database()
    
    # neighborhood = "Les Corts"
    
    for document in documents:
        if document["Nom_districte"] == neighborhood :
            print("existe") 
    

get_all_database("Les Corts")