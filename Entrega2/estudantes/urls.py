
from rest_framework.routers import DefaultRouter
from .views import EstudanteViewSet

router = DefaultRouter()
router.register("", EstudanteViewSet, basename="estudante")

urlpatterns = router.urls
