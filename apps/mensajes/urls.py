from django.urls import path
from .views import index,marcar_mensaje_leido,eliminar_mensaje

urlpatterns = [
    path('panel/mensajes/', index, name='mensajes'),
    path('panel/mensajes/<int:id_mensaje>/leido/', marcar_mensaje_leido, name='marcar_mensaje_leido'),
    path('panel/mensajes/<int:id_mensaje>/eliminar/', eliminar_mensaje, name='eliminar_mensaje'),
]
