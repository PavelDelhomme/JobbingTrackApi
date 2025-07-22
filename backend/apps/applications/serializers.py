from rest_framework import serializers
from apps.common.serializers_registry import register
from apps.common.serializers import BaseModelSerializer
from .models import (
    Application, ApplicationPlatform, ApplicationStatus,
    ApplicationType, ApplicationContract, ApplicationContractType,
    ApplicationDepartment, ApplicationPosition
)

from apps.companies.models import Company

@register(Application)
class ApplicationSerializer(BaseModelSerializer):
    # Exposer les IDs des relations pour compatibilité avec le client
    company_id = serializers.PrimaryKeyRelatedField(
        source='company',
        queryset=Company.objects.all(),
        required=False,
        allow_null=True
    )

    platform_id = serializers.PrimaryKeyRelatedField(
        source='platform',
        queryset=ApplicationPlatform.objects.all(),
        required=False,
        allow_null=True
    )

    status_id = serializers.PrimaryKeyRelatedField(
        source='status',
        queryset=ApplicationStatus.objects.all(),
        required=False,
        allow_null=True
    )

    type_id = serializers.PrimaryKeyRelatedField(
        source='type',
        queryset=ApplicationType.objects.all(),
        required=False,
        allow_null=True
    )

    contract_id = serializers.PrimaryKeyRelatedField(
        source='contract',
        queryset=ApplicationContract.objects.all(),
        required=False,
        allow_null=True
    )

    contract_type_id = serializers.PrimaryKeyRelatedField(
        source='contract_type',
        queryset=ApplicationContractType.objects.all(),
        required=False,
        allow_null=True
    )

    department_id = serializers.PrimaryKeyRelatedField(
        source='department',
        queryset=ApplicationDepartment.objects.all(),
        required=False,
        allow_null=True
    )

    position_id = serializers.PrimaryKeyRelatedField(
        source='position',
        queryset=ApplicationPosition.objects.all(),
        required=False,
        allow_null=True
    )

    class Meta(BaseModelSerializer.Meta):
        model = Application
        fields = '__all__'
        # Ajouter explicitement les champs d'ID
        read_only_fields = BaseModelSerializer.Meta.read_only_fields + [
            'company_name', # Sera mis à jour automatiquement
        ]
    
    def create(self, validated_data):
        # Extraire les objets liés des sources
        company = validated_data.pop('company', None)
        platform = validated_data.pop('platform', None)
        status = validated_data.pop('status', None)
        type_obj = validated_data.pop('type', None)
        contract = validated_data.pop('contract', None)
        contract_type = validated_data.pop('contract_type', None)
        department = validated_data.pop('department', None)
        position = validated_data.pop('position', None)

        # Créer l'application
        application = Application.objects.create(
            company=company,
            platform=platform,
            status=status,
            type=type_obj,
            contract=contract,
            contract_type=contract_type,
            department=department,
            position=position,
            **validated_data
        )

        # Mettre à jour company_name si company est fournie
        if company:
            application.company_name = company.name
            application.save()
        
        return application

    def update(self, instance, validated_data):
        # Extraire les objets liés des sources
        company = validated_data.pop('company', None)
        platform = validated_data.pop('platform', None)
        status = validated_data.pop('status', None)
        type_obj = validated_data.pop('type', None)
        contract = validated_data.pop('contract', None)
        contract_type = validated_data.pop('contract_type', None)
        department = validated_data.pop('department', None)
        position = validated_data.pop('position', None)

        # Mettre à jour les relations
        if company is not None:
            instance.company = company
            instance.company_name = company.name
        if platform is not None:
            instance.platform = platform
        if status is not None:
            instance.status = status
        if type_obj is not None:
            instance.type = type_obj
        if contract is not None:
            instance.contract = contract
        if contract_type is not None:
            instance.contract_type = contract_type
        if department is not None:
            instance.department = department
        if position is not None:
            instance.position = position
        
        # Mettre à jour les autres champs
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance