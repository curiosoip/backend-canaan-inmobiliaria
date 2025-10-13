from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('panel/administrativo', admin.site.urls),
    path('auth/', include('social_django.urls', namespace='social')),
    path('', include('apps.web.urls')),
    path('api/departamentos/', include('apps.departamentos.urls')),

]

from .admin import admin