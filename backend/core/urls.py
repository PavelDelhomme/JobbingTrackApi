from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth / JWT
    path('api/auth/',          include('apps.authentification.urls')),

    # Domaines métier
    path('api/applications/',  include('apps.applications.urls')),
    path('api/contacts/',      include('apps.contacts.urls')),
    path('api/companies/',     include('apps.companies.urls')),
    path('api/calls/',         include('apps.calls.urls')),
    path('api/calendar/',      include('apps.calendar.urls')),
    path('api/cvs/',           include('apps.cvs.urls')),
    path('api/followups/',     include('apps.followups.urls')),
    path('api/interviews/',    include('apps.interviews.urls')),
    path('api/profiles/',      include('apps.profiles.urls')),
    path('api/references/',    include('apps.references.urls')),
    path('api/events/',        include('apps.events.urls')),
]

urlpatterns += [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,  document_root=settings.MEDIA_ROOT)
