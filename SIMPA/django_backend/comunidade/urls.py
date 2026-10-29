from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PerfilUsuarioView,
    TopicoDuvidaViewSet,
    RespostaDuvidaViewSet,
    WhatsAppNotificacaoView,
)

router = DefaultRouter()
router.register("duvidas", TopicoDuvidaViewSet, basename="topico-duvida")
router.register("respostas", RespostaDuvidaViewSet, basename="resposta-duvida")

urlpatterns = [
    # IE01 — Perfil e Avatar
    path("perfil/", PerfilUsuarioView.as_view(), name="perfil_usuario"),

    # IE03 — Notificações e Auditoria WhatsApp
    path("whatsapp/", WhatsAppNotificacaoView.as_view(), name="whatsapp_notificacao"),

    # IE02 — Dúvidas e Respostas da Comunidade
    path("", include(router.urls)),
]
