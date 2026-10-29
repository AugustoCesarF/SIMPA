from django.contrib import admin
from .models import Turma, LocalAula


@admin.register(LocalAula)
class LocalAulaAdmin(admin.ModelAdmin):
    list_display = ("sala", "bloco", "campus", "andar", "cidade", "capacidade", "tipo_espaco")
    search_fields = ("sala", "bloco", "campus", "cidade")
    list_filter = ("campus", "cidade", "tipo_espaco")


@admin.register(Turma)
class TurmaAdmin(admin.ModelAdmin):
    list_display = (
        "nome",
        "codigo",
        "curso",
        "periodo",
        "professor",
        "local_aula",
        "horario",
        "ativa",
    )
    search_fields = ("nome", "codigo", "curso", "professor")
    list_filter = ("ativa", "curso", "periodo", "local_aula__bloco")
    filter_horizontal = ("estudantes",)
