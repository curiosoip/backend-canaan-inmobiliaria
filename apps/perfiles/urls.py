from django.urls import path
from .views import profile_view

urlpatterns = [
    path('perfil-usuario', profile_view, name='profile')
]