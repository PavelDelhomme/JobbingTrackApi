from rest_framework import serializers
from .models import Appel

class AppelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appel
        fields = '__all__'