
from rest_framework import viewsets
from .models import Estudante
from .serializers import EstudanteSerializer


class EstudanteViewSet(viewsets.ModelViewSet):
    queryset = Estudante.objects.all().order_by("nome")
    serializer_class = EstudanteSerializer
