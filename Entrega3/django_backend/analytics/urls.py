"""
URLs — Módulo Analítico (SIMPA Entrega 3)
"""

from django.urls import path
from . import views

app_name = "analytics"

urlpatterns = [
    # Templates (MVT — renderiza HTML)
    path("", views.dashboard_analitico, name="dashboard"),
    path("relatorio/", views.relatorio_periodo, name="relatorio"),

    # API REST JSON
    path("api/estatisticas/", views.api_estatisticas_gerais, name="api_estatisticas"),
    path("api/turma/<int:turma_id>/", views.api_estatisticas_turma, name="api_turma"),
    path("api/aluno/<int:aluno_id>/risco/", views.api_risco_aluno, name="api_risco"),
    path("api/correlacao/", views.api_correlacao, name="api_correlacao"),
]
