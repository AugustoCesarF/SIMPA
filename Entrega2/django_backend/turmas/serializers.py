
from rest_framework import serializers
from .models import Turma


class TurmaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turma
        fields = "__all__"
