from rest_framework.filters import BaseFilterBackend

class UpdatedAfterFilter(BaseFilterBackend):
    """
    ?updated_after=TIMESTAMP (secondes Unix)
    """
    def filter_queryset(self, request, queryset, view):
        since = request.query_params.get('updated_after')
        if since and since.isdigit():
            queryset = queryset.filter(updated_at__gt=int(since))
        return queryset