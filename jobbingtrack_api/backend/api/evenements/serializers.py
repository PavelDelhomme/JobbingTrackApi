from rest_framework import serializers
from .models import Event

class EvenementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
