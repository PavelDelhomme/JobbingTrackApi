from rest_framework import serializers
from .models import Relance

class RelanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relance
        fields = '__all__'
        read_only_fields = ('user',)
