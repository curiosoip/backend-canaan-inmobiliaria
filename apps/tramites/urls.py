from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_tramites, name='tramites'),
    path('registrar/', views.registrar_tramite, name='registrar_tramite'),
    path('editar/<uuid:id_tramite>/', views.editar_tramite, name='editar_tramite'),
    path('eliminar/<uuid:id_tramite>/', views.eliminar_tramite, name='eliminar_tramite'),

    path('requisitos/', views.index_requisitos, name='requisitos'),
    path('requisitos/registrar/<uuid:id_tramite>/', views.registrar_requisito, name='registrar_requisito'),
    path('requisitos/eliminar/<uuid:id_requisito_tramite>/', views.eliminar_requisito, name='eliminar_requisito'),

]
