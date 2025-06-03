from rest_framework import serializers
from .models import Event

class EvenementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': True},
            'user_id': {'read_only': True},
            'sync_hash': {'required': False},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
            'deleted_at': {'read_only': True},
            'archived_at': {'read_only': True},
            'is_archived': {'read_only': True},
            'is_deleted': {'read_only': True},
        }
