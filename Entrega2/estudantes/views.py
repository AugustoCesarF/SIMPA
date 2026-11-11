from rest_framework import viewsets, filters
from .models import Estudante
from .serializers import EstudanteSerializer


class EstudanteViewSet(viewsets.ModelViewSet):
    queryset = Estudante.objects.all().prefetch_related("turmas").order_by("nome")
    serializer_class = EstudanteSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["nome", "matricula", "cpf", "email", "curso"]
    ordering_fields = ["nome", "matricula", "criado_em"]
