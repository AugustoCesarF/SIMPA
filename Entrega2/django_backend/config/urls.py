
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/estudantes/", include("estudantes.urls")),
    path("api/turmas/", include("turmas.urls")),
    path("api/registros/", include("registros.api_urls")),
    path("", include("registros.urls")),
]
