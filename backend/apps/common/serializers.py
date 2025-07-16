from rest_framework import serializers

class BaseModelSerializer(serializers.ModelSerializer):
    """
    Serializer de base pour tous les modèles métier.
    Rend read-only les champs système.
    """
    class Meta:
        abstract = True
        read_only_fields = (
            'id',
            'created_at',
            'updated_at',
            'deleted_at',
            'archived_at',
            'user',
            'sync_hash',
        )
    
    def create(self, validated_data):
        """Ajoute l'utilisateur automatiquement à la création"""
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
