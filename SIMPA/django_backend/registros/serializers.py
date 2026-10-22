from decimal import Decimal
from rest_framework import serializers
from .models import RegistroAcademico


class RegistroAcademicoSerializer(serializers.ModelSerializer):
    estudante_nome = serializers.CharField(source="estudante.nome", read_only=True)
    estudante_matricula = serializers.CharField(source="estudante.matricula", read_only=True)
    turma_nome = serializers.CharField(source="turma.nome", read_only=True)
    turma_codigo = serializers.CharField(source="turma.codigo", read_only=True)
    situacao = serializers.SerializerMethodField(read_only=True)
    em_risco = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = RegistroAcademico
        fields = [
            "id",
            "estudante",
            "estudante_nome",
            "estudante_matricula",
            "turma",
            "turma_nome",
            "turma_codigo",
            "periodo",
            "nota",
            "frequencia",
            "situacao",
            "em_risco",
            "observacoes",
            "atualizado_em",
        ]
        read_only_fields = ["id", "atualizado_em", "estudante_nome", "estudante_matricula", "turma_nome", "turma_codigo", "situacao", "em_risco"]

    def get_situacao(self, obj):
        try:
            nota = float(obj.nota)
            freq = float(obj.frequencia)
            if freq < 75.0:
                return "Reprovado por Falta"
            elif nota >= 6.0:
                return "Aprovado"
            elif nota >= 4.0:
                return "Recuperação"
            else:
                return "Reprovado"
        except (ValueError, TypeError):
            return "Em Curso"

    def get_em_risco(self, obj):
        try:
            return float(obj.nota) < 6.0 or float(obj.frequencia) < 75.0
        except (ValueError, TypeError):
            return False

    def validate_nota(self, value):
        if value < Decimal("0.00") or value > Decimal("10.00"):
            raise serializers.ValidationError("A nota deve estar entre 0.00 e 10.00.")
        return value

    def validate_frequencia(self, value):
        if value < Decimal("0.00") or value > Decimal("100.00"):
            raise serializers.ValidationError("A frequência deve estar entre 0.00% e 100.00%.")
        return value

    def validate(self, attrs):
        estudante = attrs.get("estudante") or (self.instance.estudante if self.instance else None)
        turma = attrs.get("turma") or (self.instance.turma if self.instance else None)
        periodo = attrs.get("periodo") or (self.instance.periodo if self.instance else None)

        if estudante and turma and periodo:
            qs = RegistroAcademico.objects.filter(
                estudante=estudante,
                turma=turma,
                periodo=periodo,
            )
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError(
                    {"non_field_errors": ["Já existe um registro acadêmico para este estudante nesta turma e período."]}
                )
        return attrs
