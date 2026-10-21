
from rest_framework.routers import DefaultRouter
from .views import RegistroAcademicoViewSet

router = DefaultRouter()
router.register("", RegistroAcademicoViewSet, basename="registro-academico")

urlpatterns = router.urls
