from rest_framework import serializers
from django.contrib.auth.models import User
from .models import PerfilUsuario, TopicoDuvida, RespostaDuvida, LogNotificacaoWhatsApp


class PerfilUsuarioSerializer(serializers.ModelSerializer):
    """
    IE01 — Serializer para Visualização e Edição de Perfil e Avatar.
    """
    username = serializers.CharField(source="user.username", read_only=True)
    nome = serializers.SerializerMethodField(read_only=True)
    email = serializers.CharField(source="user.email", read_only=True)
    avatar_exibicao = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = PerfilUsuario
        fields = [
            "id",
            "username",
            "nome",
            "email",
            "avatar_url",
            "avatar_exibicao",
            "biografia",
            "telefone",
            "cidade",
            "uf",
            "matricula_ra",
            "curso",
            "notificacoes_whatsapp",
            "atualizado_em",
        ]
        read_only_fields = ["id", "username", "email", "atualizado_em", "avatar_exibicao"]

    def get_nome(self, obj):
        return obj.user.get_full_name() or obj.user.username

    def get_avatar_exibicao(self, obj):
        return obj.get_avatar_exibicao()


class RespostaDuvidaSerializer(serializers.ModelSerializer):
    """
    IE02 — Serializer para respostas da comunidade.
    """
    autor_username = serializers.CharField(source="autor.username", read_only=True)
    autor_nome = serializers.SerializerMethodField(read_only=True)
    autor_avatar = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = RespostaDuvida
        fields = [
            "id",
            "topico",
            "autor",
            "autor_username",
            "autor_nome",
            "autor_avatar",
            "conteudo",
            "eh_solucao",
            "criado_em",
            "atualizado_em",
        ]
        read_only_fields = ["id", "autor", "criado_em", "atualizado_em", "autor_username", "autor_nome", "autor_avatar"]

    def get_autor_nome(self, obj):
        return obj.autor.get_full_name() or obj.autor.username

    def get_autor_avatar(self, obj):
        if hasattr(obj.autor, "perfil"):
            return obj.autor.perfil.get_avatar_exibicao()
        return f"https://ui-avatars.com/api/?name={obj.autor.username}&background=4e8cff&color=fff"

    def validate_conteudo(self, value):
        conteudo = value.strip()
        if not conteudo:
            raise serializers.ValidationError("O conteúdo da resposta não pode ser vazio.")
        return conteudo


class TopicoDuvidaSerializer(serializers.ModelSerializer):
    """
    IE02 — Serializer para publicação e consulta de dúvidas da comunidade.
    """
    autor_username = serializers.CharField(source="autor.username", read_only=True)
    autor_nome = serializers.SerializerMethodField(read_only=True)
    autor_avatar = serializers.SerializerMethodField(read_only=True)
    turma_nome = serializers.CharField(source="turma.nome", read_only=True)
    total_respostas = serializers.SerializerMethodField(read_only=True)
    respostas = RespostaDuvidaSerializer(many=True, read_only=True)

    class Meta:
        model = TopicoDuvida
        fields = [
            "id",
            "titulo",
            "conteudo",
            "autor",
            "autor_username",
            "autor_nome",
            "autor_avatar",
            "turma",
            "turma_nome",
            "disciplina_nome",
            "resolvido",
            "total_respostas",
            "respostas",
            "criado_em",
            "atualizado_em",
        ]
        read_only_fields = [
            "id",
            "autor",
            "criado_em",
            "atualizado_em",
            "autor_username",
            "autor_nome",
            "autor_avatar",
            "turma_nome",
            "total_respostas",
            "respostas",
        ]

    def get_autor_nome(self, obj):
        return obj.autor.get_full_name() or obj.autor.username

    def get_autor_avatar(self, obj):
        if hasattr(obj.autor, "perfil"):
            return obj.autor.perfil.get_avatar_exibicao()
        return f"https://ui-avatars.com/api/?name={obj.autor.username}&background=4e8cff&color=fff"

    def get_total_respostas(self, obj):
        return obj.respostas.count()

    def validate_titulo(self, value):
        titulo = value.strip()
        if len(titulo) < 5:
            raise serializers.ValidationError("O título da dúvida deve ter no mínimo 5 caracteres.")
        return titulo

    def validate_conteudo(self, value):
        conteudo = value.strip()
        if not conteudo:
            raise serializers.ValidationError("O detalhamento da dúvida não pode ser vazio.")
        return conteudo


class LogNotificacaoWhatsAppSerializer(serializers.ModelSerializer):
    """
    IE03 — Serializer para auditoria de notificações via WhatsApp.
    """
    class Meta:
        model = LogNotificacaoWhatsApp
        fields = "__all__"
        read_only_fields = ["id", "criado_em"]
