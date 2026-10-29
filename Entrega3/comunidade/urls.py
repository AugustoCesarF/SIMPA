from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PerfilUsuarioView,
    TopicoDuvidaViewSet,
    RespostaDuvidaViewSet,
    WhatsAppNotificacaoView,
)

router = DefaultRouter()
router.register("topicos", TopicoDuvidaViewSet, basename="topico-duvida")
router.register("duvidas", TopicoDuvidaViewSet, basename="duvida")
router.register("respostas", RespostaDuvidaViewSet, basename="resposta-duvida")

urlpatterns = [
    # IE01 — Perfil e Avatar (API)
    path("perfil/", PerfilUsuarioView.as_view(), name="perfil_usuario_api"),

    # IE03 — Notificações e Auditoria WhatsApp (API)
    path("whatsapp/", WhatsAppNotificacaoView.as_view(), name="whatsapp_notificacao_api"),

    # IE02 — Dúvidas e Respostas da Comunidade (API)
    path("", include(router.urls)),
]
