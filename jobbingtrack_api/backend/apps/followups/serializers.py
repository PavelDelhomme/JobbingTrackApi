from rest_framework import serializers
from .models import FollowUp

class FollowUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowUp
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': True},
            'user_id': {'read_only': True},
            'sync_hash': {'required': False},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
            'is_deleted': {'read_only': True},
            'is_archived': {'read_only': True},
        }
