
from rest_framework import viewsets
from .models import Turma
from .serializers import TurmaSerializer


class TurmaViewSet(viewsets.ModelViewSet):
    queryset = Turma.objects.all().order_by("nome")
    serializer_class = TurmaSerializer
