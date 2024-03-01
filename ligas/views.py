from django.shortcuts import render
from .models import Equipo, Partido

def lista_equipos(request):
    equipos = Equipo.objects.all()
    return render(request, 'ligas/lista_equipos.html', {'equipos': equipos})

def detalle_equipo(request, equipo_id):
    equipo = Equipo.objects.get(pk=equipo_id)
    return render(request, 'ligas/detalle_equipo.html', {'equipo': equipo})

def lista_partidos(request):
    partidos = Partido.objects.all()
    return render(request, 'ligas/lista_partidos.html', {'partidos': partidos})
