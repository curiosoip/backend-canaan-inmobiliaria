from django.urls import path
from .views import clientes,empresas,registrar_usuario,eliminarusuario,editar_usuario,UploadFotoUsuarioView,index_roles,registrar_rol,editar_rol,eliminar_rol

urlpatterns = [
    path('clientes/', clientes, name='usuarios_clientes'),
    path('empresas/', empresas, name='usuarios_empresas'),
    path('registrar/', registrar_usuario, name='registrar_usuario'),
    path('editar/<uuid:id_usuario>/', editar_usuario, name='editar_usuario'), 
    path('eliminar/<uuid:id_usuario>/', eliminarusuario, name='eliminar_usuario'),
    path("upload-foto/", UploadFotoUsuarioView.as_view(), name="upload_foto"),

    path('roles/', index_roles, name='roles'),
    path('roles/registrar/', registrar_rol, name='registrar_rol'),
    path('roles/editar/<uuid:id_rol>/', editar_rol, name='editar_rol'),
    path('roles/eliminar/<uuid:id_rol>/', eliminar_rol, name='eliminar_rol'),
]

