from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permission personnalisée pour permettre seulement aux propriétaires
    d'un objet de le modifier.
    """
    
    def has_object_permission(self, request, view, obj):
        # Permissions de lecture pour toutes les requêtes
        if request.method in permissions.SAFE_METHODS:
            return obj.user == request.user
        
        # Permissions d'écriture seulement pour le propriétaire
        return obj.user == request.user
