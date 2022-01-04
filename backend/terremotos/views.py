from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
import requests, datetime

# from backend.terremotos.serializers import TerremotoSerializer
from terremotos.serializers import TerremotoSerializer
from rest_framework.decorators import api_view
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt


# {}
# {nombre: asas, apellido: assas}

def generate_request(url, params={}):
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()


def transformarTiempo(tiempo):
    tiempo = tiempo/1000
    date_time_obj = datetime.datetime.fromtimestamp(tiempo)
    fecha = date_time_obj.date()
    return str(fecha)

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


@csrf_exempt
@api_view(["POST"])
def crearTerremoto(request):
    try:
        serializer = TerremotoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        else:
            return JsonResponse("No se pudo crear el terremoto", safe=False, status=status.HTTP_400_BAD_REQUEST)
    except:
        return JsonResponse("No se pudo crear el terremoto", safe=False, status=status.HTTP_400_BAD_REQUEST)
    return JsonResponse(serializer.data, safe=False, status=status.HTTP_201_CREATED)