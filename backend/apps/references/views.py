from rest_framework.decorators import action
from rest_framework.response import Response
from apps.common.viewsets import BaseViewSet
from .models import Reference, ReferenceType
from .serializers import ReferenceSerializer
from rest_framework.filters import SearchFilter

class ReferenceViewSet(BaseViewSet):
    queryset = Reference.objects.all()
    serializer_class = ReferenceSerializer
    filter_backends = [SearchFilter]
    search_fields = ['label']
    
    @action(detail=False, methods=['get'])
    def by_type(self, request):
        """Récupère les références par type"""
        ref_type = request.query_params.get('type')
        if ref_type and ref_type in [choice[0] for choice in ReferenceType.choices]:
            queryset = self.get_queryset().filter(type=ref_type)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        return Response({'error': 'Type de référence invalide'}, status=400)
    
    @action(detail=False, methods=['get'])
    def types(self, request):
        """Liste tous les types de références disponibles"""
        return Response([{
            'value': choice[0],
            'label': choice[1]
        } for choice in ReferenceType.choices])
