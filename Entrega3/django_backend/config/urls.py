"""
URLs principais — SIMPA Entrega 3
Arquitetura MVT: cada app Django gerencia seu próprio bloco de URLs.
"""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),

    # APIs REST (DRF)
    path("api/estudantes/", include("estudantes.urls")),
    path("api/turmas/", include("turmas.urls")),
    path("api/registros/", include("registros.api_urls")),

    # Módulo Analítico — Entrega 3 (Views + API JSON)
    path("analytics/", include("analytics.urls")),

    # Dashboard principal e rotas legadas
    path("", include("registros.urls")),
]
