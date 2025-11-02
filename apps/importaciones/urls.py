from django.urls import path
from .views import index_importaciones, registrar_importacion, editar_importacion, eliminar_importacion
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', login_required(index_importaciones), name='importaciones'),
    path('registrar/', registrar_importacion, name='registrar_importacion'),
    path('editar/<uuid:id_importacion>/', editar_importacion, name='editar_importacion'),
    path('eliminar/<uuid:id_importacion>/', eliminar_importacion, name='eliminar_importacion'),
]
