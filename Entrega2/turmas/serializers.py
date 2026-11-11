from rest_framework import serializers
from .models import Turma, LocalAula
from estudantes.models import Estudante


class EstudanteSimplesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estudante
        fields = ["id", "nome", "matricula", "email", "ativo"]


class LocalAulaSerializer(serializers.ModelSerializer):
    """
    IE04 — Serializer para Cadastro e Visualização do Local de Aula.
    """
    class Meta:
        model = LocalAula
        fields = "__all__"

    def validate_sala(self, value):
        sala = value.strip()
        if not sala:
            raise serializers.ValidationError("A identificação da sala é obrigatória.")
        return sala

    def validate_bloco(self, value):
        bloco = value.strip()
        if not bloco:
            raise serializers.ValidationError("O bloco/prédio é obrigatório.")
        return bloco


class TurmaSerializer(serializers.ModelSerializer):
    total_estudantes = serializers.SerializerMethodField(read_only=True)
    estudantes_detalhes = EstudanteSimplesSerializer(source="estudantes", many=True, read_only=True)
    local_aula_detalhes = LocalAulaSerializer(source="local_aula", read_only=True)
    estudantes = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Estudante.objects.all(),
        required=False,
    )
    local_aula = serializers.PrimaryKeyRelatedField(
        queryset=LocalAula.objects.all(),
        required=False,
        allow_null=True,
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
            "local_aula",
            "local_aula_detalhes",
            "horario",
            "dia_semana",
            "link_grupo_whatsapp",
            "ativa",
            "criada_em",
            "total_estudantes",
            "estudantes",
            "estudantes_detalhes",
        ]
        read_only_fields = ["id", "criada_em", "total_estudantes", "estudantes_detalhes", "local_aula_detalhes"]

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
