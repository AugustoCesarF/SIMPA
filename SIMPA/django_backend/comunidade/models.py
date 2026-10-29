from django.db import models
from django.contrib.auth.models import User


class PerfilUsuario(models.Model):
    """
    IE01 — Avatar e Perfil do Usuário autenticado.
    Permite visualização e edição de bio, avatar, telefone e dados acadêmicos.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="perfil")
    avatar_url = models.CharField(
        max_length=500,
        blank=True,
        default="",
        help_text="URL da imagem de avatar do perfil",
    )
    biografia = models.TextField(blank=True, default="", help_text="Breve descrição ou bio do usuário")
    telefone = models.CharField(max_length=30, blank=True, default="", help_text="Telefone / WhatsApp com DDD")
    cidade = models.CharField(max_length=100, blank=True, default="Anápolis")
    uf = models.CharField(max_length=2, blank=True, default="GO")
    matricula_ra = models.CharField(max_length=30, blank=True, default="", help_text="RA ou identificação funcional")
    curso = models.CharField(max_length=150, blank=True, default="Inteligência Artificial")
    notificacoes_whatsapp = models.BooleanField(
        default=True,
        help_text="IE03 — Aceita receber alertas e lembretes via WhatsApp",
    )
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Perfil de {self.user.username} ({self.user.get_full_name() or 'Sem nome'})"

    def get_avatar_exibicao(self):
        """Retorna avatar configurado ou gera avatar dinâmico com base nas iniciais."""
        if self.avatar_url:
            return self.avatar_url
        nome = self.user.get_full_name() or self.user.username
        return f"https://ui-avatars.com/api/?name={nome.replace(' ', '+')}&background=4e8cff&color=fff"

    class Meta:
        verbose_name = "Perfil de Usuário"
        verbose_name_plural = "Perfis de Usuários"


class TopicoDuvida(models.Model):
    """
    IE02 — Comunidade: Publicação de dúvidas e tópicos de discussão.
    """
    titulo = models.CharField(max_length=200, help_text="Título da dúvida")
    conteudo = models.TextField(help_text="Detalhamento da dúvida ou pergunta")
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="topicos_duvida")
    turma = models.ForeignKey(
        "turmas.Turma",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="topicos_duvida",
        help_text="Turma relacionada à dúvida",
    )
    disciplina_nome = models.CharField(max_length=150, blank=True, default="", help_text="Nome da disciplina")
    resolvido = models.BooleanField(default=False)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"[{self.disciplina_nome or 'Geral'}] {self.titulo} (por {self.autor.username})"

    class Meta:
        ordering = ["-criado_em"]
        verbose_name = "Tópico de Dúvida"
        verbose_name_plural = "Tópicos de Dúvidas"


class RespostaDuvida(models.Model):
    """
    IE02 — Comunidade: Respostas para as dúvidas publicadas.
    """
    topico = models.ForeignKey(TopicoDuvida, on_delete=models.CASCADE, related_name="respostas")
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="respostas_duvida")
    conteudo = models.TextField(help_text="Texto da resposta")
    eh_solucao = models.BooleanField(default=False, help_text="Marcada como resposta aceita pelo autor ou professor")
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Resposta de {self.autor.username} no tópico '{self.topico.titulo[:30]}'"

    class Meta:
        ordering = ["criado_em"]
        verbose_name = "Resposta de Comunidade"
        verbose_name_plural = "Respostas de Comunidade"


class LogNotificacaoWhatsApp(models.Model):
    """
    IE03 — Registro oficial de notificações via WhatsApp (Meta Cloud API).
    Preserva rastreabilidade e registra dependências de autorização externa.
    """
    destinatario_nome = models.CharField(max_length=150)
    destinatario_telefone = models.CharField(max_length=30)
    estudante = models.ForeignKey(
        "estudantes.Estudante",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="logs_whatsapp",
    )
    turma = models.ForeignKey(
        "turmas.Turma",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="logs_whatsapp",
    )
    tipo_notificacao = models.CharField(max_length=60, default="ALERTA_RISCO")
    mensagem = models.TextField()
    template_utilizado = models.CharField(max_length=100, default="simpa_alerta_academico")
    status_envio = models.CharField(
        max_length=60,
        default="PENDENTE_AUTORIZACAO_API",
        help_text="Status do envio: ENVIADO, PENDENTE_AUTORIZACAO_API ou ERRO",
    )
    meta_message_id = models.CharField(max_length=120, blank=True, default="")
    resposta_api = models.TextField(blank=True, default="")
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"WhatsApp para {self.destinatario_nome} ({self.status_envio}) em {self.criado_em.strftime('%d/%m/%Y %H:%M')}"

    class Meta:
        ordering = ["-criado_em"]
        verbose_name = "Log de Notificação WhatsApp"
        verbose_name_plural = "Logs de Notificações WhatsApp"
