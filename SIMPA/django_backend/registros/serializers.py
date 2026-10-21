
from rest_framework import serializers
from .models import RegistroAcademico


class RegistroAcademicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroAcademico
        fields = "__all__"
