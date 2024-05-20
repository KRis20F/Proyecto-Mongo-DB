import matplotlib
matplotlib.use('Agg') 
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
import os

def connect_database():
    uri = "mongodb+srv://reifa:rafa@contaminacion.4m05tim.mongodb.net/?retryWrites=true&w=majority&appName=contaminacion"
    client = MongoClient(uri, server_api=ServerApi('1'))
    try:
        client.admin.command('ping')
        return client["ContaminacionBCN"], client
    
    except Exception as error:
        print(error)
        return None, None

def search_results(neighborhood, date):
    search_result = []
    db, client = connect_database()

    estacion_id = get_neighborhood_id(db, neighborhood)

    if estacion_id:
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
        client.close()
        return None

def get_neighborhood_id(db, neighborhood):
    id_document = db.Estaciones.find_one({"Nom_barri": neighborhood})

    if id_document:
        return id_document.get("Estacio")
    else:
        return None

def get_neighborhood_list():
    neighborhood_list = []

    db, client = connect_database()

    neighborhoods = db.Estaciones.distinct("Nom_barri")

    for neighborhood in neighborhoods:
        neighborhood_list.append(neighborhood)
        print(neighborhood)

    client.close()

    return neighborhood_list


# Estadisticas

def calcular_estadisticas(search_result):
    stats = defaultdict(lambda: {"values": [], "mean": 0, "max": 0, "min": 0})

    for data in search_result:
        contaminant = data["desc"]
        value = data["result"]
        if value != "":
            value = float(value)
            stats[contaminant]["values"].append(value)
    
    for contaminant, values in stats.items():
        if values["values"]:
            values["mean"] = np.mean(values["values"])
            values["max"] = np.max(values["values"])
            values["min"] = np.min(values["values"])

    return stats

def generar_grafico(stats, neighborhood):
    fig, ax = plt.subplots()

    contaminantes = list(stats.keys())
    means = [stats[contaminante]["mean"] for contaminante in contaminantes]
    maxs = [stats[contaminante]["max"] for contaminante in contaminantes]
    mins = [stats[contaminante]["min"] for contaminante in contaminantes]

    x = np.arange(len(contaminantes))

    ax.bar(x - 0.2, means, 0.2, label='Promedio')
    ax.bar(x, maxs, 0.2, label='Máximo')
    ax.bar(x + 0.2, mins, 0.2, label='Mínimo')

    ax.set_xlabel('Contaminante')
    ax.set_ylabel('Valores')
    ax.set_title(f'Estadísticas de Contaminación en {neighborhood} durante Marzo')
    ax.set_xticks(x)
    ax.set_xticklabels(contaminantes, rotation=45, ha="right")
    ax.legend()

    fig.tight_layout()

     # Asegurarse de que el subdirectorio static/img existe
    img_dir = os.path.join(os.path.dirname(__file__), 'static', 'img')
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)

    # Guardar la imagen en static/img
    filename = f'estadisticas_{neighborhood}.png'
    image_path = os.path.join(img_dir, filename)
    plt.savefig(image_path)
    plt.close(fig)

    return filename