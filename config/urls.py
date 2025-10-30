from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('panel/administrativo', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('apps.web.urls')),
    path('api/departamentos/', include('apps.departamentos.urls')),

]

from .admin import admin