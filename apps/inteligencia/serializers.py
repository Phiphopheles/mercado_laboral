from rest_framework import serializers
from .models import RecomendacionTarea, PrediccionHabilidad

class RecomendacionTareaSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecomendacionTarea
        fields = '__all__'

class PrediccionHabilidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrediccionHabilidad
        fields = '__all__'
