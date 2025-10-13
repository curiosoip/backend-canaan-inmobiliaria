# apps/departamentos/api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count, Q
from apps.departamentos.models import Departamento
from .serializers import DepartamentoSerializer

class DepartamentoListView(APIView):
    def get(self, request):
        departamentos = (
            Departamento.objects.annotate(
                total_viviendas=Count('viviendas', distinct=True),
                total_urbanizaciones=Count('urbanizaciones', distinct=True),
                total_tramites=Count('tramites', distinct=True)
            )
            .filter(
                Q(total_viviendas__gt=0) |
                Q(total_urbanizaciones__gt=0) |
                Q(total_tramites__gt=0)
            )
            .order_by('nombre')
        )

        serializer = DepartamentoSerializer(departamentos, many=True)
        return Response(serializer.data)
