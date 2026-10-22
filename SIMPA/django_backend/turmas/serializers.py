from rest_framework import serializers
from .models import Turma
from estudantes.models import Estudante


class EstudanteSimplesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estudante
        fields = ["id", "nome", "matricula", "email", "ativo"]


class TurmaSerializer(serializers.ModelSerializer):
    total_estudantes = serializers.SerializerMethodField(read_only=True)
    estudantes_detalhes = EstudanteSimplesSerializer(source="estudantes", many=True, read_only=True)
    estudantes = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Estudante.objects.all(),
        required=False,
    )

    class Meta:
        model = Turma
        fields = [
            "id",
            "nome",
            "codigo",
            "curso",
            "periodo",
            "professor",
            "carga_horaria",
            "ativa",
            "criada_em",
            "total_estudantes",
            "estudantes",
            "estudantes_detalhes",
        ]
        read_only_fields = ["id", "criada_em", "total_estudantes", "estudantes_detalhes"]

    def get_total_estudantes(self, obj):
        return obj.estudantes.count()

    def validate_nome(self, value):
        nome = value.strip()
        if not nome:
            raise serializers.ValidationError("O nome da turma é obrigatório.")
        return nome

    def validate_codigo(self, value):
        codigo = value.strip().upper()
        if not codigo:
            raise serializers.ValidationError("O código da disciplina/turma é obrigatório.")
        qs = Turma.objects.filter(codigo=codigo)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("Já existe uma turma cadastrada com este código.")
        return codigo

    def validate_curso(self, value):
        curso = value.strip()
        if not curso:
            raise serializers.ValidationError("O curso é obrigatório.")
        return curso

    def validate_periodo(self, value):
        periodo = value.strip()
        if not periodo:
            raise serializers.ValidationError("O período é obrigatório.")
        return periodo
