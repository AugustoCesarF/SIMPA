from django.contrib import admin
from .models import SnapshotEstatistico


@admin.register(SnapshotEstatistico)
class SnapshotEstatisticoAdmin(admin.ModelAdmin):
    list_display = (
        "periodo",
        "turma",
        "media_notas",
        "desvio_padrao_notas",
        "taxa_aprovacao",
        "correlacao_nota_frequencia",
        "calculado_em",
    )
    list_filter = ("periodo", "turma")
    readonly_fields = ("calculado_em",)
    ordering = ("-calculado_em",)
