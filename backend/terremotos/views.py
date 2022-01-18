from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
import requests, datetime
from terremotos.models import Terremoto

# from backend.terremotos.serializers import TerremotoSerializer
from terremotos.serializers import TerremotoSerializer
from rest_framework.decorators import api_view
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt

# Import general
import numpy as np
from django.db.models import Avg, Max

# -------------------------------------------------------------------
# ------------------------ MAGNITUD ---------------------------------
# -------------------------------------------------------------------

def obtener_lista_terremoto(terremotos):
    lista_terremotos = terremotos.all().order_by('-tiempo')[0:20] # Obtengo lista de los ultimos 20 terremotos
    serializer_lista = TerremotoSerializer(lista_terremotos,many = True)
    return serializer_lista

# Calculo de minimo
def calculo_min_magnitud(terremotos):
    terremotos_min = terremotos.order_by('magnitud')[0:25]
    serializer = TerremotoSerializer(terremotos_min, many = True)
    for i in serializer.data:
        if i['magnitud'] != None:
            return i

# Calculo de maximo
def calculo_max_magnitud(terremotos):
    terremotos_max = terremotos.order_by('-magnitud')[0:25]
    serializer = TerremotoSerializer(terremotos_max, many = True)
    for i in serializer.data:
        if i['magnitud'] != None:
            return i

# Calculo de media
def calculo_media_magnitud(terremotos):
    media = terremotos.aggregate(Avg('magnitud'))
    return media

# Calculo de mediana
def calculo_mediana_magnitud(terremotos):
  
    serializer = TerremotoSerializer(terremotos, many = True)

    lista_magnitudes = []
    for i in serializer.data:
        if i['magnitud'] != None:
            lista_magnitudes.append(i['magnitud'])

    mediana = np.percentile(lista_magnitudes,50)

    return mediana

# ----------------------------------------------------------------------
# ------------------------ PROFUNDIDAD ---------------------------------
# ----------------------------------------------------------------------

# Calculo de minimo
def calculo_min_profundidad(terremotos):
    terremotos_min = terremotos.order_by('profundidad')[0:25]
    serializer = TerremotoSerializer(terremotos_min, many = True)
    for i in serializer.data:
        if i['profundidad'] != None:
            return i

# Calculo de maximo
def calculo_max_profundidad(terremotos):
    terremotos_max = terremotos.order_by('-profundidad')[0:25]
    serializer = TerremotoSerializer(terremotos_max, many = True)
    for i in serializer.data:
        if i['profundidad'] != None:
            return i

# Calculo de media
def calculo_media_profundidad(terremotos):
    media = terremotos.aggregate(Avg('profundidad'))
    return media

# Calculo de mediana
def calculo_mediana_profundidad(terremotos):
  
    serializer = TerremotoSerializer(terremotos, many = True)

    lista_profundidades = []
    for i in serializer.data:
        if i['profundidad'] != None:
            lista_profundidades.append(i['profundidad'])

    mediana = np.percentile(lista_profundidades,50)

    return mediana

# ----------------------------------------------------------------------
# ------------------------------ OTROS ---------------------------------
# ----------------------------------------------------------------------

def transformarTiempo(tiempo):
    tiempo = tiempo/1000
    date_time_obj = datetime.datetime.fromtimestamp(tiempo)
    fecha = date_time_obj.date()
    return str(fecha)

def generate_request(url, params={}):
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()

@api_view(["POST"])
def obtener(request):
    try:
        parametros = {
            "format": "geojson"
        }
        response = generate_request('https://earthquake.usgs.gov/fdsnws/event/1/query',parametros)
        p1 = response["features"]
        L = []
        for i in p1:
            terremoto = {
                "magnitud": i["properties"]["mag"],
                "lugar": i["properties"]["place"],
                "tiempo": transformarTiempo(i["properties"]["time"]),
                "tsunami": i["properties"]["tsunami"],
                "importancia": i["properties"]["sig"],
                "fecha_actualizacion": transformarTiempo(i["properties"]["updated"]),
                "alerta": i["properties"]["alert"],
                "dispersion_profundidad": i["properties"]["dmin"],
                # "Profundidad": i["properties"]["depth"]
                "tipo_movimiento": i["properties"]["type"]
            }
            L.append(terremoto)

        terremoto = TerremotoSerializer(data=L,many=True)
        if terremoto.is_valid():
           terremoto.save()
        
        return HttpResponse("Se ingresaron correctamente")
    except:
        return HttpResponse("No se hizo nada")

#--------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------

#                                   PÁGINAS

def inicio(request):
    # terremotos = Terremoto.objects.all().order_by('-tiempo')[0:20]

    terremotos = Terremoto.objects.all()

    # Obtencion lista pricipal
    lista_terremotos = obtener_lista_terremoto(terremotos)

    # -------------------- MAGNITUD -----------------------------
    # Obtencion minimo
    terremotos_min_mag = calculo_min_magnitud(terremotos)
    # Obtencion maximo
    terremotos_max_mag = calculo_max_magnitud(terremotos)
    # Obtencion media
    media_mag = calculo_media_magnitud(terremotos)
    # Obtencion mediana
    mediana_mag = calculo_mediana_magnitud(terremotos)

    # -------------------- PROFUNDIDAD --------------------------
    # Obtencion minimo
    terremotos_min_pro = calculo_min_profundidad(terremotos)
    # Obtencion maximo
    terremotos_max_pro = calculo_max_profundidad(terremotos)
    # Obtencion media
    media_pro = calculo_media_profundidad(terremotos)
    # Obtencion mediana
    mediana_pro = calculo_mediana_profundidad(terremotos)

    # Guardar resultados
    resultado = {
        'terremotos': lista_terremotos.data,
        'magnitud': {
            'terremoto_min_mag': terremotos_min_mag,
            'terremoto_max_mag': terremotos_max_mag,
            'media_mag': media_mag,
            'mediana_mag': mediana_mag
        },
        'profundidad': {
            'terremoto_min_pro': terremotos_min_pro,
            'terremoto_max_pro': terremotos_max_pro,
            'media_pro': media_pro,
            'mediana_pro': mediana_pro
        } 
    }
    return render(request,"terremotos/inicio.html",resultado)


