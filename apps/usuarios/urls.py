from django.urls import path
from .views import clientes,empresas,reset_password_form,registrar_usuario,reset_password_usuario,eliminarusuario_empresa,eliminarusuario_cliente,editar_usuario,UploadFotoUsuarioView,index_roles,registrar_rol,editar_rol,eliminar_rol

urlpatterns = [
    path('clientes/', clientes, name='usuarios_clientes'),
    path('empresas/', empresas, name='usuarios_empresas'),
    path('registrar/', registrar_usuario, name='registrar_usuario'),
    path('editar/<uuid:id_usuario>/', editar_usuario, name='editar_usuario'), 
    path('eliminar/empresa/<uuid:id_usuario>/', eliminarusuario_empresa, name='eliminar_usuario_empresa'),
    path('eliminar/cliente/<uuid:id_usuario>/', eliminarusuario_cliente, name='eliminar_usuario_cliente'),
    path("upload-foto/", UploadFotoUsuarioView.as_view(), name="upload_foto"),

    path('roles/', index_roles, name='roles'),
    path('roles/registrar/', registrar_rol, name='registrar_rol'),
    path('roles/editar/<uuid:id_rol>/', editar_rol, name='editar_rol'),
    path('roles/eliminar/<uuid:id_rol>/', eliminar_rol, name='eliminar_rol'),

    path('reset-password/<uuid:id_usuario>/', reset_password_usuario, name='reset_password_usuario'),
    path('reset-password-form/', reset_password_form, name='reset_password_form'),
]

