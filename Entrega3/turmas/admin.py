
from django.contrib import admin
from .models import Turma


@admin.register(Turma)
class TurmaAdmin(admin.ModelAdmin):
    list_display = (
        "nome",
        "codigo",
        "curso",
        "periodo",
        "professor",
        "ativa",
    )
    search_fields = ("nome", "codigo", "curso", "professor")
    list_filter = ("ativa", "curso", "periodo")
    filter_horizontal = ("estudantes",)
