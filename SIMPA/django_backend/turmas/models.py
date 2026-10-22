
from django.db import models


class Turma(models.Model):
    nome = models.CharField(max_length=150)
    codigo = models.CharField(max_length=30, unique=True)
    curso = models.CharField(max_length=150)
    periodo = models.CharField(max_length=30)
    professor = models.CharField(max_length=150, blank=True)
    carga_horaria = models.PositiveIntegerField(default=60)
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
