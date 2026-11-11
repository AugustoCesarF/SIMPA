import re
from rest_framework import serializers
from .models import Estudante


def validar_cpf(cpf: str) -> bool:
    """Valida número de CPF conforme algoritmo oficial da Receita Federal."""
    numeros = re.sub(r"\D", "", str(cpf))
    if len(numeros) != 11:
        return False
    if numeros == numeros[0] * 11:
        return False

    soma = sum(int(numeros[i]) * (10 - i) for i in range(9))
    resto = (soma * 10) % 11
    d1 = 0 if resto == 10 else resto
    if int(numeros[9]) != d1:
        return False

    soma = sum(int(numeros[i]) * (11 - i) for i in range(10))
    resto = (soma * 10) % 11
    d2 = 0 if resto == 10 else resto
    return int(numeros[10]) == d2


class EstudanteSerializer(serializers.ModelSerializer):
    turmas_detalhes = serializers.SerializerMethodField(read_only=True)
    turma_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = Estudante
        fields = [
            "id",
            "nome",
            "matricula",
            "cpf",
            "data_nascimento",
            "email",
            "telefone",
            "curso",
            "ativo",
            "criado_em",
            "turmas_detalhes",
            "turma_id",
        ]
        read_only_fields = ["id", "criado_em", "turmas_detalhes"]

    def get_turmas_detalhes(self, obj):
        return [
            {"id": t.id, "codigo": t.codigo, "nome": t.nome}
            for t in obj.turmas.all()
        ]

    def validate_nome(self, value):
        nome = value.strip()
        if len(nome) < 2:
            raise serializers.ValidationError("O nome completo deve conter pelo menos 2 caracteres.")
        return nome

    def validate_matricula(self, value):
        matricula = value.strip()
        if not matricula:
            raise serializers.ValidationError("A matrícula é obrigatória.")
        # Se for update, ignorar o próprio estudante
        qs = Estudante.objects.filter(matricula=matricula)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("Já existe um estudante cadastrado com esta matrícula.")
        return matricula

    def validate_email(self, value):
        email = value.strip()
        if not email:
            raise serializers.ValidationError("O e-mail é obrigatório.")
        return email

    def validate_curso(self, value):
        curso = value.strip()
        if not curso:
            raise serializers.ValidationError("O curso é obrigatório.")
        return curso

    def validate_cpf(self, value):
        if not value:
            return ""
        cpf_limpo = re.sub(r"\D", "", value)
        if not validar_cpf(cpf_limpo):
            raise serializers.ValidationError("CPF inválido. Forneça 11 dígitos válidos.")
        return cpf_limpo

    def create(self, validated_data):
        turma_id = validated_data.pop("turma_id", None)
        estudante = Estudante.objects.create(**validated_data)
        if turma_id:
            from turmas.models import Turma
            turma = Turma.objects.filter(id=turma_id).first()
            if turma:
                turma.estudantes.add(estudante)
        return estudante

    def update(self, instance, validated_data):
        turma_id = validated_data.pop("turma_id", None)
        estudante = super().update(instance, validated_data)
        if turma_id:
            from turmas.models import Turma
            turma = Turma.objects.filter(id=turma_id).first()
            if turma:
                turma.estudantes.add(estudante)
        return estudante
