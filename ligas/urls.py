from django.urls import path
from . import views

urlpatterns = [
    path('equipos/', views.lista_equipos, name='lista_equipos'),
    path('equipos/<int:equipo_id>/', views.detalle_equipo, name='detalle_equipo'),
    path('partidos/', views.lista_partidos, name='lista_partidos'),
]
