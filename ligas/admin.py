from typing import Any
from django.contrib import admin
from django.db.models.fields.related import ForeignKey
from django.forms.models import ModelChoiceField
from django.http import HttpRequest

# Register your models here.
from .models import *

class PartitAdmin(admin.ModelAdmin):
    # 👇 eso peta
    list_display = ('equip_local', 'equip_visitant', 'resultat_equip_local', 'resultat_equip_visitant')
    print("hola")

admin.site.register(Liga)
admin.site.register(Equipo)
admin.site.register(Jugador)
# admin.site.register(Partido)
admin.site.register(Event)

#? Event:
class EventInline(admin.TabularInline):
	model = Event
	fields = ["temps","tipus","jugador","equip"]
	ordering = ("temps",)
	def formfield_for_foreignkey(self, db_field: Any, request: HttpRequest, **kwargs: Any) -> ModelChoiceField:
		if db_field.name == "equip":
			partit_id = request.resolver_match.kwargs["object_id"]
			partit = Partido.objects.get(id=partit_id)
			equips_ids = [partit.local.id,partit.visitant.id]
			qs = Jugador.objects.filter(equip__id__in=equips_ids)
			kwargs["queryset"] = qs

		elif db_field.name == "jugador":
			partit_id = request.resolver_match.kwargs["object_id"]
			partit = Partido.objects.get(id=partit_id)
			jugadors_local = [j.id for j in partit.local.jugador_set.all()]
			jugadors_visitant = [j.id for j in partit.visitant.jugador_set.all()]
			jugadors = jugadors_local + jugadors_visitant
			kwargs["queryset"] = Jugador.objects.filter(id__in=jugadors)

		return super().formfield_for_foreignkey(db_field, request, **kwargs)

class PartitAdmin(admin.ModelAdmin):
        # podem fer cerques en els models relacionats
        # (noms dels equips o títol de la lliga)
	search_fields = ["local__nom","visitant__nom","lliga__titol"]
        # el camp personalitzat ("resultats" o recompte de gols)
        # el mostrem com a "readonly_field"
	readonly_fields = ["resultat",]
	list_display = ["local","visitant","resultat","lliga","inici"]
	ordering = ("-inici",)
	inlines = [EventInline,]
	def resultat(self,obj):
		gols_local = obj.event_set.filter(
		                tipus=Event.EventType.GOL,
                                equip=obj.local).count()
		gols_visit = obj.event_set.filter(
		                tipus=Event.EventType.GOL,
                                equip=obj.visitant).count()
		return "{} - {}".format(gols_local,gols_visit)
 
admin.site.register(Partido,PartitAdmin)