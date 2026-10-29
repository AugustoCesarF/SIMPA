
from django.contrib import admin
from .models import RegistroAcademico


@admin.register(RegistroAcademico)
class RegistroAcademicoAdmin(admin.ModelAdmin):
    list_display = (
        "estudante",
        "turma",
        "periodo",
        "nota",
        "frequencia",
        "atualizado_em",
    )
    search_fields = (
        "estudante__nome",
        "estudante__matricula",
        "turma__nome",
        "turma__codigo",
    )
    list_filter = ("periodo", "turma")
