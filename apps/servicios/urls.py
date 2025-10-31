from django.urls import path
from .views import index, registrar_servicio, editar_servicio, eliminar_servicio
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', login_required(index), name='servicios'),
    path('registrar/', registrar_servicio, name='registrar_servicio'),
    path('editar/<uuid:id_servicio>/', editar_servicio, name='editar_servicio'),
    path('eliminar/<uuid:id_servicio>/', eliminar_servicio, name='eliminar_servicio'),
]
