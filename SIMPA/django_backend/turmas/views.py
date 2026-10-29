from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Turma, LocalAula
from .serializers import TurmaSerializer, LocalAulaSerializer, EstudanteSimplesSerializer
from estudantes.models import Estudante


class LocalAulaViewSet(viewsets.ModelViewSet):
    """
    IE04 — CRUD de Locais de Aula (Campus, Bloco, Sala, Capacidade).
    """
    queryset = LocalAula.objects.all().order_by("campus", "bloco", "sala")
    serializer_class = LocalAulaSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["campus", "bloco", "sala", "cidade", "tipo_espaco"]
    ordering_fields = ["bloco", "sala", "capacidade"]


class TurmaViewSet(viewsets.ModelViewSet):
    queryset = Turma.objects.all().select_related("local_aula").prefetch_related("estudantes").order_by("nome")
    serializer_class = TurmaSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["nome", "codigo", "curso", "professor", "periodo", "local_aula__sala", "local_aula__bloco"]
    ordering_fields = ["nome", "codigo", "criada_em"]

    @action(detail=True, methods=["post"], url_path="matricular")
    def matricular_aluno(self, request, pk=None):
        turma = self.get_object()
        estudante_id = request.data.get("estudante_id")
        matricula = request.data.get("matricula")

        estudante = None
        if estudante_id:
            estudante = Estudante.objects.filter(id=estudante_id).first()
        elif matricula:
            estudante = Estudante.objects.filter(matricula=str(matricula).strip()).first()

        if not estudante:
            return Response(
                {"error": "Estudante não encontrado. Informe 'estudante_id' ou 'matricula' válido."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if turma.estudantes.filter(id=estudante.id).exists():
            return Response(
                {"message": f"Estudante '{estudante.nome}' já está matriculado nesta turma."},
                status=status.HTTP_200_OK,
            )

        turma.estudantes.add(estudante)
        return Response(
            {
                "message": f"Estudante '{estudante.nome}' matriculado com sucesso na turma '{turma.nome}'.",
                "total_estudantes": turma.estudantes.count(),
            },
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["post"], url_path="desmatricular")
    def desmatricular_aluno(self, request, pk=None):
        turma = self.get_object()
        estudante_id = request.data.get("estudante_id")
        matricula = request.data.get("matricula")

        estudante = None
        if estudante_id:
            estudante = Estudante.objects.filter(id=estudante_id).first()
        elif matricula:
            estudante = Estudante.objects.filter(matricula=str(matricula).strip()).first()

        if not estudante:
            return Response(
                {"error": "Estudante não encontrado."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if not turma.estudantes.filter(id=estudante.id).exists():
            return Response(
                {"error": f"Estudante '{estudante.nome}' não está matriculado nesta turma."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        turma.estudantes.remove(estudante)
        return Response(
            {
                "message": f"Estudante '{estudante.nome}' desmatriculado da turma '{turma.nome}'.",
                "total_estudantes": turma.estudantes.count(),
            },
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["get"], url_path="alunos")
    def listar_alunos(self, request, pk=None):
        turma = self.get_object()
        alunos = turma.estudantes.all().order_by("nome")
        serializer = EstudanteSimplesSerializer(alunos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"], url_path="local")
    def local_aula(self, request, pk=None):
        """
        IE04 — Visualização dos detalhes do local e horário da aula da turma.
        """
        turma = self.get_object()
        if not turma.local_aula:
            return Response(
                {
                    "turma": turma.nome,
                    "codigo": turma.codigo,
                    "horario": turma.horario,
                    "dia_semana": turma.dia_semana,
                    "local": None,
                    "aviso": "Local de aula presencial ainda não alocado para esta turma.",
                    "link_whatsapp": turma.link_grupo_whatsapp or None,
                },
                status=status.HTTP_200_OK,
            )

        serializer = LocalAulaSerializer(turma.local_aula)
        return Response(
            {
                "turma": turma.nome,
                "codigo": turma.codigo,
                "horario": turma.horario,
                "dia_semana": turma.dia_semana,
                "local": serializer.data,
                "link_whatsapp": turma.link_grupo_whatsapp or None,
            },
            status=status.HTTP_200_OK,
        )
