
from django.db import models


class Estudante(models.Model):
    nome = models.CharField(max_length=150)
    matricula = models.CharField(max_length=30, unique=True)
    cpf = models.CharField(max_length=14, blank=True, default="")
    data_nascimento = models.DateField(null=True, blank=True)
    email = models.EmailField(blank=True)
    telefone = models.CharField(max_length=20, blank=True, default="")
    curso = models.CharField(max_length=150)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome} ({self.matricula})"

    class Meta:
        ordering = ["nome"]
        verbose_name = "Estudante"
        verbose_name_plural = "Estudantes"
