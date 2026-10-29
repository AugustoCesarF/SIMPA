from rest_framework import viewsets, filters, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .models import PerfilUsuario, TopicoDuvida, RespostaDuvida, LogNotificacaoWhatsApp
from .serializers import (
    PerfilUsuarioSerializer,
    TopicoDuvidaSerializer,
    RespostaDuvidaSerializer,
    LogNotificacaoWhatsAppSerializer,
)
from .services import WhatsAppService
from estudantes.models import Estudante
from turmas.models import Turma


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Permite edição/exclusão apenas ao autor ou a administradores."""
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if getattr(view, "action", None) == "responder":
            return True
        return obj.autor == request.user or request.user.is_staff


# ---------------------------------------------------------------------------
# IE01 — Avatar e Perfil do Usuário
# ---------------------------------------------------------------------------
class PerfilUsuarioView(APIView):
    """
    IE01 — Consulta e Edição do Perfil e Avatar do usuário autenticado.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        perfil, _ = PerfilUsuario.objects.get_or_create(user=request.user)
        serializer = PerfilUsuarioSerializer(perfil)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        perfil, _ = PerfilUsuario.objects.get_or_create(user=request.user)
        serializer = PerfilUsuarioSerializer(perfil, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        return self.put(request)


# ---------------------------------------------------------------------------
# IE02 — Comunidade: Dúvidas e Respostas
# ---------------------------------------------------------------------------
class TopicoDuvidaViewSet(viewsets.ModelViewSet):
    """
    IE02 — Publicação e Consulta de Dúvidas na Comunidade.
    """
    queryset = TopicoDuvida.objects.select_related("autor", "turma").prefetch_related("respostas__autor").all()
    serializer_class = TopicoDuvidaSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["titulo", "conteudo", "disciplina_nome", "turma__nome", "autor__username"]
    ordering_fields = ["criado_em", "resolvido"]

    def perform_create(self, serializer):
        serializer.save(autor=self.request.user)

    @action(detail=True, methods=["post"], url_path="responder")
    def responder(self, request, pk=None):
        topico = self.get_object()
        conteudo = request.data.get("conteudo", "").strip()
        if not conteudo:
            return Response({"error": "O conteúdo da resposta é obrigatório."}, status=status.HTTP_400_BAD_REQUEST)

        resposta = RespostaDuvida.objects.create(
            topico=topico,
            autor=request.user,
            conteudo=conteudo,
            eh_solucao=request.data.get("eh_solucao", False),
        )
        serializer = RespostaDuvidaSerializer(resposta)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"], url_path="marcar-resolvido")
    def marcar_resolvido(self, request, pk=None):
        topico = self.get_object()
        if topico.autor != request.user and not request.user.is_staff:
            return Response({"error": "Apenas o autor da dúvida ou professor pode marcá-la como resolvida."}, status=status.HTTP_403_FORBIDDEN)

        topico.resolvido = not topico.resolvido
        topico.save()
        return Response({"resolvido": topico.resolvido, "mensagem": "Status do tópico atualizado com sucesso."}, status=status.HTTP_200_OK)


class RespostaDuvidaViewSet(viewsets.ModelViewSet):
    """
    IE02 — Gerenciamento de Respostas individuais.
    """
    queryset = RespostaDuvida.objects.select_related("autor", "topico").all()
    serializer_class = RespostaDuvidaSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(autor=self.request.user)


# ---------------------------------------------------------------------------
# IE03 — Integração WhatsApp (Notificações e Status Oficial Meta)
# ---------------------------------------------------------------------------
class WhatsAppNotificacaoView(APIView):
    """
    IE03 — Envio oficial de Notificação via WhatsApp e Auditoria de Grupos.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Retorna o status da integração e os logs recentes de notificação."""
        service = WhatsAppService()
        logs = LogNotificacaoWhatsApp.objects.all()[:20]
        serializer = LogNotificacaoWhatsAppSerializer(logs, many=True)

        return Response(
            {
                "integracao_oficial": "Meta WhatsApp Business Cloud API (Graph API v19.0)",
                "configurado": service.is_configured(),
                "phone_number_id_definido": bool(service.phone_number_id),
                "politica_meta_grupos": (
                    "Conforme as diretrizes oficiais da Meta, a WhatsApp Business Cloud API "
                    "não suporta o envio programático automático de templates para grupos públicos. "
                    "Para grupos de turmas, a solução homologada pela plataforma consiste na "
                    "disponibilização do link de convite oficial (https://chat.whatsapp.com/...) "
                    "através do cadastro de cada turma (IE04) ou canais de transmissão autorizados."
                ),
                "total_notificacoes_registradas": LogNotificacaoWhatsApp.objects.count(),
                "logs_recentes": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        """
        Dispara uma notificação de risco ou aviso acadêmico via WhatsApp.
        """
        destinatario_nome = request.data.get("destinatario_nome")
        destinatario_telefone = request.data.get("destinatario_telefone")
        aluno_id = request.data.get("aluno_id")
        turma_id = request.data.get("turma_id")
        motivo_risco = request.data.get("motivo_risco", "")
        recomendacao = request.data.get("recomendacao", "")

        aluno = None
        if aluno_id:
            aluno = Estudante.objects.filter(id=aluno_id).first()
            if aluno and not destinatario_nome:
                destinatario_nome = aluno.nome
            if aluno and not destinatario_telefone and aluno.telefone:
                destinatario_telefone = aluno.telefone

        if not destinatario_nome or not destinatario_telefone:
            return Response(
                {"error": "Informe 'destinatario_nome' e 'destinatario_telefone' (ou 'aluno_id' cadastrado com telefone)."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        turma = Turma.objects.filter(id=turma_id).first() if turma_id else None

        service = WhatsAppService()
        resultado = service.enviar_notificacao_risco(
            destinatario_nome=destinatario_nome,
            destinatario_telefone=destinatario_telefone,
            aluno=aluno,
            turma=turma,
            motivo_risco=motivo_risco,
            recomendacao=recomendacao,
        )

        return Response(resultado, status=status.HTTP_200_OK if resultado.get("sucesso") else status.HTTP_502_BAD_GATEWAY)
