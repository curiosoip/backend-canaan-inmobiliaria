from django.urls import path,include
from .views import index,login_view
from django.contrib.auth.views import LogoutView



urlpatterns = [
    path('', index, name='inicio'),
    path('panel/perfiles/', include('apps.perfiles.urls')),
    path('panel/usuarios/', include('apps.usuarios.urls')),
    path('panel/mensajes/', include('apps.mensajes.urls')),
    path('panel/reportes/', include('apps.reportes.urls')),
    path('panel/servicios/', include('apps.servicios.urls')),
    path('panel/ventas/', include('apps.ventas.urls')),
    path('login', login_view, name='login'),
    path('logout', LogoutView.as_view(next_page='login'), name='logout'),
]