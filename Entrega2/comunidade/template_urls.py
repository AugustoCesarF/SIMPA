from django.urls import path
from .views import perfil_template_view, duvidas_template_view, locais_template_view

app_name = "comunidade_ui"

urlpatterns = [
    # IE01 — Avatar e Perfil do Usuário (Template HTML)
    path("perfil/", perfil_template_view, name="perfil"),

    # IE02 — Sistema de Comunidade e Dúvidas (Template HTML)
    path("duvidas/", duvidas_template_view, name="duvidas"),

    # IE04 + IE03 — Exibição de Localização de Aula e Grupos WhatsApp (Template HTML)
    path("locais/", locais_template_view, name="locais"),
]
