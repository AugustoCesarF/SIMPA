
from rest_framework.routers import DefaultRouter
from .views import TurmaViewSet

router = DefaultRouter()
router.register("", TurmaViewSet, basename="turma")

urlpatterns = router.urls
