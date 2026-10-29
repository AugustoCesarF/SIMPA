"""
Model — Módulo Analítico (SIMPA Entrega 3)

Armazena snapshots de indicadores estatísticos calculados,
permitindo consulta rápida sem recalcular a cada requisição.
"""

from django.db import models


class SnapshotEstatistico(models.Model):
    """
    Registro calculado de indicadores estatísticos por período.
    Criado (ou atualizado) sempre que os dados de registros mudam.
    """

    periodo = models.CharField(max_length=30, db_index=True)
    turma = models.ForeignKey(
        "turmas.Turma",
        on_delete=models.CASCADE,
        related_name="snapshots",
        null=True,
        blank=True,
        help_text="Nulo = indicadores gerais (todos as turmas)",
    )

    # --- Indicadores de tendência central ---
    media_notas = models.FloatField(default=0.0)
    mediana_notas = models.FloatField(default=0.0)

    # --- Indicadores de dispersão ---
    desvio_padrao_notas = models.FloatField(default=0.0)
    coef_variacao = models.FloatField(
        default=0.0, help_text="Coeficiente de variação (%)"
    )

    # --- Percentis ---
    percentil_25 = models.FloatField(default=0.0)
    percentil_75 = models.FloatField(default=0.0)

    # --- Frequência ---
    media_frequencia = models.FloatField(default=0.0)

    # --- Correlação ---
    correlacao_nota_frequencia = models.FloatField(
        default=0.0, help_text="Coeficiente de Pearson (-1 a 1)"
    )

    # --- Situação ---
    total_alunos = models.IntegerField(default=0)
    total_aprovados = models.IntegerField(default=0)
    total_recuperacao = models.IntegerField(default=0)
    total_reprovados = models.IntegerField(default=0)
    taxa_aprovacao = models.FloatField(default=0.0, help_text="Em %")

    calculado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-calculado_em"]
        verbose_name = "Snapshot Estatístico"
        verbose_name_plural = "Snapshots Estatísticos"
        constraints = [
            models.UniqueConstraint(
                fields=["periodo", "turma"],
                name="snapshot_unico_periodo_turma",
            )
        ]

    def __str__(self):
        turma_str = self.turma.codigo if self.turma else "GERAL"
        return f"Snapshot {turma_str} — {self.periodo}"
