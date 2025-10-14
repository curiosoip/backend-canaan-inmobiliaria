# apps/departamentos/api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count, Q, Prefetch
from apps.departamentos.models import Departamento
from apps.urbanizaciones.models import Urbanizacion
from apps.viviendas.models import Vivienda
from apps.tramites.models import Tramite
from .serializers import DepartamentoSerializer
from django.db import models


class DepartamentoListView(APIView):
    def get(self, request):
        nombre = request.query_params.get('nombre')
        id_departamento = request.query_params.get('id')
        tipo = request.query_params.get('tipo') 

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
            .prefetch_related(
                Prefetch('urbanizaciones', queryset=Urbanizacion.objects.all().order_by('nombre')),
                Prefetch('viviendas', queryset=Vivienda.objects.all().order_by('nombre')),
                Prefetch('tramites', queryset=Tramite.objects.filter(departamento__isnull=False).order_by('nombre'))
            )


            .order_by('nombre')
        )
        if nombre:
            departamentos = departamentos.filter(nombre__icontains=nombre)
        if id_departamento:
            departamentos = departamentos.filter(id_departamento=id_departamento)

        serializer = DepartamentoSerializer(departamentos, many=True)
        data = serializer.data

        if tipo in ["urbanizaciones", "viviendas", "tramites"]:
            for d in data:
                for rel in ["urbanizaciones", "viviendas", "tramites"]:
                    if rel != tipo:
                        d.pop(rel, None)

        return Response(data)
