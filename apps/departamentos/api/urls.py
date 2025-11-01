from django.urls import path
from apps.departamentos.views import DepartamentoListView

urlpatterns = [
    path('', DepartamentoListView.as_view(), name='departamento-list'),
]
