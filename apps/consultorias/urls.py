from django.urls import path
from .views import index_consultorias, registrar_consultoria, editar_consultoria, eliminar_consultoria
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', login_required(index_consultorias), name='consultorias'),
    path('registrar/', registrar_consultoria, name='registrar_consultoria'),
    path('editar/<uuid:id_consultoria>/', editar_consultoria, name='editar_consultoria'),
    path('eliminar/<uuid:id_consultoria>/', eliminar_consultoria, name='eliminar_consultoria'),
]
