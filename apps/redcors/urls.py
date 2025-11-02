# apps/redcors/urls.py
from django.urls import path
from .views import index_redcors, registrar_redcors, editar_redcors, eliminar_redcors
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', login_required(index_redcors), name='redcors'),
    path('registrar/', registrar_redcors, name='registrar_redcors'),
    path('editar/<uuid:id_redcors>/', editar_redcors, name='editar_redcors'),
    path('eliminar/<uuid:id_redcors>/', eliminar_redcors, name='eliminar_redcors'),
]
