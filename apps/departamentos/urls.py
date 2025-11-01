from django.urls import path
from .views import (
    index_departamentos,
    registrar_departamento,
    editar_departamento,
    eliminar_departamento,
)

urlpatterns = [
    path('', index_departamentos, name='departamentos'),
    path('registrar/', registrar_departamento, name='registrar_departamento'),
    path('editar/<uuid:id_departamento>/', editar_departamento, name='editar_departamento'),
    path('eliminar/<uuid:id_departamento>/', eliminar_departamento, name='eliminar_departamento'),
]
