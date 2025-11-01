from django.urls import path
from .views import (
    index_proceso_interno,
    registrar_proceso_interno,
    eliminar_proceso_interno,
    editar_proceso_interno,
    registrar_paso_proceso_interno,
    eliminar_paso_proceso_interno,
    index_proceso,
    registrar_proceso,
    eliminar_proceso,
    editar_proceso
)
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('internos/', login_required(index_proceso_interno), name='procesos_internos'),
    path('internos/registrar/', login_required(registrar_proceso_interno), name='registrar_proceso_interno'),
    path('internos/eliminar/<uuid:id_proceso_interno>/', login_required(eliminar_proceso_interno), name='eliminar_proceso_interno'),
    path('internos/editar/<uuid:id_proceso_interno>/', login_required(editar_proceso_interno), name='editar_proceso_interno'),

    path('internos/<uuid:id_proceso_interno>/subproceso/registrar/', login_required(registrar_paso_proceso_interno), name='registrar_paso_proceso_interno'),
    path('internos/subproceso/eliminar/<uuid:id_paso>/', login_required(eliminar_paso_proceso_interno), name='eliminar_paso_proceso_interno'),
    
    path('', login_required(index_proceso), name='procesos'),
    path('registrar/', login_required(registrar_proceso), name='registrar_proceso'),
    path('eliminar/<uuid:id_proceso>/', login_required(eliminar_proceso), name='eliminar_proceso'),
    path('editar/<uuid:id_proceso>/', login_required(editar_proceso), name='editar_proceso'),
]
