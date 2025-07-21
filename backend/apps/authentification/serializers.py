from rest_framework import serializers
from .models import User, UserPermissions
from apps.common.serializers_registry import register

@register(User)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model  = User
        fields = ('id', 'email', 'first_name', 'last_name', 'is_active', 'is_staff')


class RegistrationSerializer(serializers.ModelSerializer):
    """Inscription : renvoie user + tokens."""
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model  = User
        fields = ('email', 'password', 'first_name', 'last_name')

    def create(self, validated):
        user = User.objects.create_user(
            email=validated['email'],
            password=validated['password'],
            first_name=validated.get('first_name', ''),
            last_name=validated.get('last_name', '')
        )
        UserPermissions.objects.create(user=user)  # rôle = CLIENT par défaut
        return user

class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

class ResetSerializer(serializers.Serializer):
    token = serializers.CharField()
    new_password = serializers.CharField(min_length=8)

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(min_length=8)
    new_password = serializers.CharField(min_length=8)