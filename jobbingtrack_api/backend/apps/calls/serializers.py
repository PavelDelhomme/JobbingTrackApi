#backend/apps/calls/serializers.py
from rest_framework import serializers
from .models import Call

class CallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Call
        fields = '__all__'

        extra_kwargs = {
            'id': {'read_only': True},
            'sync_hash': {'required': False},
            'user_id': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
            'is_deleted': {'read_only': True},
            'is_archived': {'read_only': True},
        }
