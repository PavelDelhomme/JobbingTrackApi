from apps.common.viewsets import BaseViewSet

def crud_viewset(model, serializer):
    class _ViewSet(BaseViewSet):
        queryset = model.objects.all()
        serializer_class = serializer
    return _ViewSet