from collections import defaultdict

_SERIALIZER_REGISTRY = defaultdict(dict)

def register(model_cls):
    """
    Décorateur :
        @register(MyModel)
        class MyModelSerializer(...):...
    Enregistre un référence vers le serializer pour get_serializer_for_model().
    """
    def decorator(serializer_cls):
        _SERIALIZER_REGISTRY[model_cls] = serializer_cls
        return serializer_cls
    return decorator

def get_serializer_for_model(model_cls):
    return _SERIALIZER_REGISTRY.get(model_cls)