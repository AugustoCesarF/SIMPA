from rest_framework.routers import DefaultRouter
from .views import TurmaViewSet, LocalAulaViewSet

router = DefaultRouter()
router.register("locais", LocalAulaViewSet, basename="local-aula")
router.register("", TurmaViewSet, basename="turma")

urlpatterns = router.urls
