from django.urls import path, include

urlpatterns = [
    path('candidatures/', include('api.candidatures.urls')),
    path('entretiens/', include('api.entretiens.urls')),
    path('entreprises/', include('api.entreprises.urls')),
    path('relances/', include('api.relances.urls')),
    path('evenements/', include('api.evenements.urls')),
    path('contacts/', include('api.contacts.urls')),
    path('appels/', include('api.appels.urls')),
    path('profiles/', include('api.profiles.urls')),
]
