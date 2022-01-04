from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
import requests

# from backend.terremotos.serializers import TerremotoSerializer
from terremotos.serializers import TerremotoSerializer
from .services import get_username
from rest_framework.decorators import api_view

def hello_user(requests):
    context = {
        'name': get_username()
    }
    return render(requests, 'hello_user.html', context)

def hello_user(requests):
    params = { 'order': 'desc' }

    context = {
        'name': get_username(params)
    }
    return render(requests, 'hello_user.html', context)

# {}
# {nombre: asas, apellido: assas}

def generate_request(url, params={}):
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()




@api_view(["GET"])
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
                "tiempo": i["properties"]["time"],
                "tsunami": i["properties"]["tsunami"],
                "importancia": i["properties"]["sig"],
                "fecha_actualizacion": i["properties"]["updated"],
                "alerta": i["properties"]["alert"],
                "dispersion_profundidad": i["properties"]["dmin"],
                # "Profundidad": i["properties"]["depth"]
                "tipo_movimiento": i["properties"]["type"]
            }
            L.append(terremoto)
    
        # Ingresar a la base de datos
        return JsonResponse(L[0],safe=False)
        for i in L:
            terremoto = TerremotoSerializer(data=i)
            if terremoto.is_valid():
                terremoto.save()
            else:
                return HttpResponse("Los terremotos no han sido ingresados")
        
        return JsonResponse(L,safe=False)
    except:
        return HttpResponse("No se hizo nada")