from django.db import models


class LocalAula(models.Model):
    """
    IE04 — Cadastro e Gestão do Local Físico da Aula.
    Representa o campus, prédio/bloco e sala/laboratório onde a aula é ministrada.
    """
    campus = models.CharField(max_length=150, default="UniEVANGÉLICA - Campus Anápolis")
    bloco = models.CharField(max_length=60, help_text="Ex: Bloco A, Bloco de Exatas")
    sala = models.CharField(max_length=60, help_text="Ex: Sala 204, Lab de IA 02")
    andar = models.CharField(max_length=40, blank=True, help_text="Ex: 2º Andar")
    cidade = models.CharField(max_length=100, default="Anápolis")
    uf = models.CharField(max_length=2, default="GO")
    capacidade = models.PositiveIntegerField(default=45)
    tipo_espaco = models.CharField(max_length=60, default="Sala de Aula", help_text="Ex: Sala de Aula, Laboratório, Auditório")
    observacoes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.sala} ({self.bloco}) - {self.campus}"

    class Meta:
        ordering = ["campus", "bloco", "sala"]
        verbose_name = "Local de Aula"
        verbose_name_plural = "Locais de Aula"


class Turma(models.Model):
    nome = models.CharField(max_length=150)
    codigo = models.CharField(max_length=30, unique=True)
    curso = models.CharField(max_length=150)
    periodo = models.CharField(max_length=30)
    professor = models.CharField(max_length=150, blank=True)
    carga_horaria = models.PositiveIntegerField(default=60)
    local_aula = models.ForeignKey(
        LocalAula,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="turmas",
        help_text="IE04 — Local onde a aula é ministrada",
    )
    horario = models.CharField(max_length=100, blank=True, default="19:00 - 22:30", help_text="Horário da aula")
    dia_semana = models.CharField(max_length=50, blank=True, default="Segunda-feira", help_text="Dia da semana da aula")
    link_grupo_whatsapp = models.URLField(max_length=300, blank=True, default="", help_text="IE03 — Link oficial do grupo de WhatsApp da turma")
    estudantes = models.ManyToManyField(
        "estudantes.Estudante",
        blank=True,
        related_name="turmas",
    )
    ativa = models.BooleanField(default=True)
    criada_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.codigo} - {self.nome}"

    class Meta:
        ordering = ["nome"]
        verbose_name = "Turma"
        verbose_name_plural = "Turmas"
