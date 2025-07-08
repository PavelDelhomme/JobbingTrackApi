from django.urls import path, include

urlpatterns = [
    path('candidatures/', include('apps.candidatures.urls')),
    path('entretiens/', include('apps.entretiens.urls')),
    path('entreprises/', include('apps.entreprises.urls')),
    path('relances/', include('apps.relances.urls')),
    path('evenements/', include('apps.evenements.urls')),
    path('contacts/', include('apps.contacts.urls')),
    path('appels/', include('apps.appels.urls')),
    path('profiles/', include('apps.profiles.urls')),
    path('auth/', include('authentication.urls')),
]
