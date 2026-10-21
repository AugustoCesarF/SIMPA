
from django.contrib import admin
from .models import Estudante


@admin.register(Estudante)
class EstudanteAdmin(admin.ModelAdmin):
    list_display = ("nome", "matricula", "email", "curso", "ativo")
    search_fields = ("nome", "matricula", "email", "curso")
    list_filter = ("ativo", "curso")
