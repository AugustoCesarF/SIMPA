
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class RegistroAcademico(models.Model):
    estudante = models.ForeignKey(
        "estudantes.Estudante",
        on_delete=models.PROTECT,
        related_name="registros_academicos",
    )
    turma = models.ForeignKey(
        "turmas.Turma",
        on_delete=models.PROTECT,
        related_name="registros_academicos",
    )
    periodo = models.CharField(max_length=30)
    nota = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10),
        ],
    )
    frequencia = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ],
    )
    observacoes = models.TextField(blank=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.estudante} - {self.turma} ({self.periodo})"

    class Meta:
        ordering = ["estudante__nome"]
        verbose_name = "Registro acadêmico"
        verbose_name_plural = "Registros acadêmicos"
        constraints = [
            models.UniqueConstraint(
                fields=["estudante", "turma", "periodo"],
                name="registro_unico_estudante_turma_periodo",
            )
        ]
