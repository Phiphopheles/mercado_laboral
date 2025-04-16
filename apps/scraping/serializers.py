from rest_framework import serializers
from .models import OfertaEmpleo

class OfertaEmpleoSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfertaEmpleo
        fields = '__all__'
