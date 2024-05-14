from pymongo import MongoClient
from pymongo.server_api import ServerApi

def connect_database():
    uri = "mongodb+srv://reifa:rafa@contaminacion.4m05tim.mongodb.net/?retryWrites=true&w=majority&appName=contaminacion"
    client = MongoClient(uri, server_api=ServerApi('1'))
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        return client
    except Exception as e:
        print(e)
        return None

def search_results(neighborhood, date):
    search_result = []
    estacion_id = get_neighborhood_id(neighborhood)

    if estacion_id:
        client = connect_database()
        db = client["ContaminacionBCN"]
        
        info_calidad = db.CalidadAire.find({"ESTACIO": estacion_id, "DIA": date})

        for result in info_calidad:
            data = {}

            info_cont = db.Contaminantes.find_one({"Codi_Contaminant": result["CODI_CONTAMINANT"]})

            data["result"] = result["H12"]
            data["desc"] = info_cont["Desc_Contaminant"]
            data["uni"] = info_cont["Unitats"]

            search_result.append(data)

        for value in search_result:
            print(f"{value['desc']}: {value['result']} {value['uni']}")

        client.close()

        return search_result
    else:
        return None

def get_neighborhood_id(neighborhood):
    client = connect_database()
    db = client["ContaminacionBCN"]
    id_document = db.Estaciones.find_one({"Nom_barri": neighborhood})
    client.close()

    if id_document:
        return id_document.get("Estacio")
    else:
        return None
    
    
def get_date_id():
    client = connect_database()
    db = client["ContaminacionBCN"]
    

# Ejemplo de uso:
# neighborhood = "Sants"
# date = 3
# search_results(neighborhood, date)


# def get_data_neighborhood(neighborhood):
    
#     client = connect_database()
    
#     db = client["ContaminacionBCN"]
    
#     db = db.Estaciones.find_one({"Nom_barri": neighborhood})
    
#     for document in db:
#         data_neighborhood = document.get("Nom_barri")
#         return data_neighborhood
            