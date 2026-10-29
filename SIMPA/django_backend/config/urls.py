from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
from config.auth_views import LoginTokenView, LogoutTokenView, MeView
from registros.views import api_indicadores, api_relatorios, api_risco_aluno
from comunidade.views import PerfilUsuarioView

urlpatterns = [
    path("admin/", admin.site.urls),

    # RF08 — Autenticação por token
    path("api/auth/token/", LoginTokenView.as_view(), name="auth_token_login"),
    path("api/auth/login/", LoginTokenView.as_view(), name="auth_login"),
    path("api/auth/logout/", LogoutTokenView.as_view(), name="auth_logout"),
    path("api/auth/me/", MeView.as_view(), name="auth_me"),
    path("api-token-auth/", obtain_auth_token, name="api_token_auth"),

    # RF07 — Recursos da API REST
    path("api/estudantes/", include("estudantes.urls")),
    path("api/alunos/", include("estudantes.urls")),
    path("api/turmas/", include("turmas.urls")),
    path("api/registros/", include("registros.api_urls")),

    # IE01 — Avatar e Perfil
    path("api/perfil/", PerfilUsuarioView.as_view(), name="api_perfil"),

    # IE02 e IE03 — Comunidade e Integração WhatsApp
    path("api/comunidade/", include("comunidade.urls")),

    # Indicadores, Relatórios e Predição de Risco
    path("api/indicadores/", api_indicadores, name="api_indicadores"),
    path("api/relatorios/", api_relatorios, name="api_relatorios"),
    path("api/risco/<int:aluno_id>/", api_risco_aluno, name="api_risco_aluno"),

    # Interface Web e Rotas de Compatibilidade
    path("", include("registros.urls")),
]
