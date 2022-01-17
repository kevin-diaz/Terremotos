import string
from kafka import KafkaConsumer
from json import loads
from datetime import datetime
from json import dumps
import psycopg2

def transformarTiempo(tiempo):
    tiempo = tiempo/1000
    date_time_obj = datetime.fromtimestamp(tiempo)
    fecha = date_time_obj.date()
    return str(fecha)

consumer = KafkaConsumer(
    'dist',
     bootstrap_servers=['localhost:9092'],
     auto_offset_reset='earliest',
     enable_auto_commit=True,
     group_id='my-group',
     value_deserializer=lambda x: loads(x.decode('utf-8')))

conn = psycopg2.connect(database="distribuidos", user='postgres', password='pass', host='127.0.0.1', port= '5500')
cursor = conn.cursor()

for message in consumer:
    message = message.value
    # print(message)
    if not isinstance(message["tiempo"],str):
        message["tiempo"] = transformarTiempo(message["tiempo"])
    if not isinstance(message["fecha_actualizacion"],str):
        message["fecha_actualizacion"] = transformarTiempo(message["fecha_actualizacion"])

    try:
        cursor.execute("INSERT INTO terremotos_terremoto (id,magnitud,lugar,tiempo,tsunami,importancia,fecha_actualizacion,alerta,dispersion_profundidad,tipo_movimiento,profundidad) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", 
        (message["identificador"],message["magnitud"],message["lugar"],message["tiempo"],message["tsunami"],message["importancia"],message["fecha_actualizacion"],message["alerta"],message["dispersion_profundidad"],message["tipo_movimiento"],message["profundidad"]))
        conn.commit()
    except:
        # print("Me salté la wea")
        pass
    # print("Guardé el Json en la BD")

conn.close()

