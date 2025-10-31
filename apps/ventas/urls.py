from django.urls import path
from .views import index_ventas, registrar_venta, eliminar_venta
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', login_required(index_ventas), name='ventas'),
    path('registrar/', login_required(registrar_venta), name='registrar_venta'),
    path('eliminar/<uuid:id_venta>/', login_required(eliminar_venta), name='eliminar_venta'),
]
