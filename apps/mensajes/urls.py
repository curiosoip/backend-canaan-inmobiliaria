from django.urls import path
from .views import index,marcar_mensaje_leido,eliminar_mensaje

urlpatterns = [
    path('', index, name='mensajes'),
    path('leido/<int:id_mensaje>/', marcar_mensaje_leido, name='marcar_mensaje_leido'),
    path('eliminar/<int:id_mensaje>/', eliminar_mensaje, name='eliminar_mensaje'),
]
