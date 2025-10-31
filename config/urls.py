from django.contrib import admin
from django.urls import path,include
from apps.mensajes.views import crear_mensaje

urlpatterns = [
    path('panel/administrativo', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('apps.web.urls')),
    path('api/departamentos/', include('apps.departamentos.urls')),
    path('api/mensajes/', crear_mensaje,name="crear_mensaje"),
]

from .admin import admin