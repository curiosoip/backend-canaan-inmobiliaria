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
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import DepartamentoForm
from django.core.paginator import Paginator


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


@login_required
def index_departamentos(request):
    departamentos=Departamento.objects.all().order_by('-fecha_registro')
    context = {
        "banner_title": "Departamentos",
        "departamentos": departamentos,
        "total_registros": departamentos.count()
    }
    return render(request, 'admin/departamentos/index.html', context)


@login_required
def registrar_departamento(request):
    if request.method == 'POST':
        form = DepartamentoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Departamento registrado correctamente.")
            return redirect('departamentos')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = DepartamentoForm()

    context = {
        'form': form,
        'banner_title': 'Registrar Departamento'
    }
    return render(request, 'admin/departamentos/index.html', context)


@login_required
def editar_departamento(request, id_departamento):
    departamento = get_object_or_404(Departamento, id_departamento=id_departamento)

    if request.method == 'POST':
        form = DepartamentoForm(request.POST, instance=departamento)
        if form.is_valid():
            form.save()
            messages.success(request, "Departamento actualizado correctamente.")
            return redirect('departamentos')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = DepartamentoForm(instance=departamento)

    context = {
        'form': form,
        'departamento': departamento,
        'banner_title': 'Editar Departamento'
    }
    return render(request, 'admin/departamentos/index.html', context)


@login_required
def eliminar_departamento(request, id_departamento):
    departamento = get_object_or_404(Departamento, id_departamento=id_departamento)
    try:
        departamento.delete()
        messages.success(request, "Departamento eliminado correctamente.")
    except Exception as e:
        messages.error(request, f"Error al eliminar el departamento: {str(e)}")
    return redirect('departamentos')