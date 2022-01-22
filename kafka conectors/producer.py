from time import sleep
from json import dumps
from kafka import KafkaProducer 
import requests
from datetime import datetime

producer = KafkaProducer(bootstrap_servers=['172.20.0.4:9093'],
                         value_serializer=lambda x:
                         dumps(x).encode('utf-8'))

for i in range(120): #60 Minutes
    response = requests.get('https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson')
    
    r = response.json()
    lista_terremotos = []
    for i in r["features"]:
        terremoto = {
            "identificador": i["id"],
            "magnitud": i["properties"]["mag"],
            "lugar": i["properties"]["place"],
            "tiempo": i["properties"]["time"],
            "tsunami": i["properties"]["tsunami"],
            "importancia": i["properties"]["sig"],
            "fecha_actualizacion": i["properties"]["updated"],
            "alerta": i["properties"]["alert"],
            "dispersion_profundidad": i["properties"]["dmin"],
            "profundidad": i["geometry"]["coordinates"][2],
            "tipo_movimiento": i["properties"]["type"]
        }
        lista_terremotos.append(terremoto)

    data = {
        "actualizacion": r["metadata"]["generated"],
        "terremotos": lista_terremotos
    }  
    # print("Produje")
    for i in data["terremotos"]:
        producer.send('dist',value = i)
    sleep(60)