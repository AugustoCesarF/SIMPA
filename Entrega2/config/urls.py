"""
URLs principais — SIMPA Entrega 3
Arquitetura MVT: cada app Django gerencia seu próprio bloco de URLs e templates.
"""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),

    # APIs REST (Django REST Framework)
    path("api/estudantes/", include("estudantes.urls")),
    path("api/turmas/", include("turmas.urls")),
    path("api/registros/", include("registros.api_urls")),
    path("api/comunidade/", include("comunidade.urls")),

    # Módulo Analítico — Entrega 3 (MVT: Dashboard + Relatórios + API Stats)
    path("analytics/", include("analytics.urls")),

    # Módulo Comunidade & Vida Universitária (IE01, IE02, IE03, IE04 - Templates HTML)
    path("comunidade/", include("comunidade.template_urls")),

    # Dashboard principal e rotas legadas
    path("", include("registros.urls")),
]
