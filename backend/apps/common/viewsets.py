from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrReadOnly

class BaseViewSet(viewsets.ModelViewSet):
    """
    ViewSet de base pour tous les modèles métier.
    Filtre automatiquement par utilisateur et gère le soft delete.
    """
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    
    def get_queryset(self):
        """Filtre par utilisateur et exclut les éléments supprimés"""
        return self.queryset.filter(
            user=self.request.user,
            is_deleted=False
        )
    
    def perform_create(self, serializer):
        """Associe l'utilisateur lors de la création"""
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def soft_delete(self, request, pk=None):
        """Suppression logique"""
        obj = self.get_object()
        obj.soft_delete()
        return Response({'status': 'deleted'})
    
    @action(detail=True, methods=['post'])
    def archive(self, request, pk=None):
        """Archivage"""
        obj = self.get_object()
        obj.archive()
        return Response({'status': 'archived'})
    
    @action(detail=True, methods=['post'])
    def restore(self, request, pk=None):
        """Restauration"""
        obj = self.get_object()
        obj.restore()
        return Response({'status': 'restored'})
    
    @action(detail=False, methods=['get'])
    def archived(self, request):
        """Liste des éléments archivés"""
        queryset = self.queryset.filter(
            user=request.user,
            is_archived=True,
            is_deleted=False
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def deleted(self, request):
        """Liste des éléments supprimés"""
        queryset = self.queryset.filter(
            user=request.user,
            is_deleted=True
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
