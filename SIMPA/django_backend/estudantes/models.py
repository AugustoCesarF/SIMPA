
from django.db import models


class Estudante(models.Model):
    nome = models.CharField(max_length=150)
    matricula = models.CharField(max_length=30, unique=True)
    email = models.EmailField(blank=True)
    curso = models.CharField(max_length=150)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome} ({self.matricula})"

    class Meta:
        ordering = ["nome"]
        verbose_name = "Estudante"
        verbose_name_plural = "Estudantes"
