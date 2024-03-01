from django.db import models

class Liga(models.Model):
    nombre = models.CharField(max_length=100)
    pais = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Equipo(models.Model):
    nombre = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=100)
    fundacion = models.DateField()
    liga = models.ForeignKey(Liga, on_delete=models.CASCADE, related_name='equipos')

    def __str__(self):
        return self.nombre

class Jugador(models.Model):
    nombre = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    posicion = models.CharField(max_length=50)
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name='jugadores')

    def __str__(self):
        return self.nombre

class Partido(models.Model):
    class Meta:
        unique_together = ["local","visitant","lliga"]
    local = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name="partits_local", default=None)
    visitant = models.ForeignKey(Equipo,on_delete=models.CASCADE,
                    related_name="partits_visitant", default=None)
    lliga = models.ForeignKey(Liga, on_delete=models.CASCADE, default=None)
    detalls = models.TextField(null=True,blank=True)
    inici = models.DateTimeField(null=True,blank=True)
    def __str__(self):
        return "{} - {}".format(self.local,self.visitant)
    
    def gols_local(self):
        return self.event_set.filter(
            tipus=Event.EventType.GOL,equipo=self.local
        ).count()
    
    def gols_visitant(self):
        return self.event_set.filter(
            tipus=Event.EventType.GOL,equipo=self.visitant
        ).count()

class Event(models.Model):
    # el tipus d'event l'implementem amb algo tipus "enum"
    class EventType(models.TextChoices):
        GOL = "GOL"
        AUTOGOL = "AUTOGOL"
        FALTA = "FALTA"
        PENALTY = "PENALTY"
        MANS = "MANS"
        CESSIO = "CESSIO"
        FORA_DE_JOC = "FORA_DE_JOC"
        ASSISTENCIA = "ASSISTENCIA"
        TARGETA_GROGA = "TARGETA_GROGA"
        TARGETA_VERMELLA = "TARGETA_VERMELLA"
    Partido = models.ForeignKey(Partido,on_delete=models.CASCADE)
    temps = models.TimeField()
    tipus = models.CharField(max_length=30,choices=EventType.choices)
    jugador = models.ForeignKey(Jugador,null=True,
                    on_delete=models.SET_NULL,
                    related_name="events_fets")
    equipo = models.ForeignKey(Equipo,null=True,
                    on_delete=models.SET_NULL)
    # per les faltes
    jugador2 = models.ForeignKey(Jugador,null=True,blank=True,
                    on_delete=models.SET_NULL,
                    related_name="events_rebuts")
    detalls = models.TextField(null=True,blank=True)
