from apps.common.viewsets import BaseViewSet

def crud_viewset(model, serializer, *, on_create=None, on_update=None,
                 extra_backends=None, search_fields=None):
    """
    Retourne un ViewSet prêt à l’emploi.
    - on_create(obj)   : callback après création
    - on_update(obj)   : callback après update
    - extra_backends   : liste de FilterBackends supplémentaires
    - search_fields    : liste des champs recherchables
    """
    class _VS(BaseViewSet):
        queryset = model.objects.all()
        serializer_class = serializer

        if extra_backends:
            filter_backends = BaseViewSet.filter_backends + list(extra_backends)
        if search_fields:
            locals()['search_fields'] = search_fields     # injecte l’attribut

        def perform_create(self, serializer):
            obj = serializer.save(user=self.request.user)
            if on_create:
                on_create(obj)

        def perform_update(self, serializer):
            obj = serializer.save()
            if on_update:
                on_update(obj)

    _VS.__name__ = f"{model.__name__}ViewSet"
    return _VS