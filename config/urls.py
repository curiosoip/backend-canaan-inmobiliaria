from django.contrib import admin
from django.urls import path,include
from apps.web.views import login_redirect

urlpatterns = [
    path('panel/administrativo', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('login-redirect/', login_redirect),
    path('', include('apps.web.urls')),
    path('api/departamentos/', include('apps.departamentos.urls')),

]

from .admin import admin