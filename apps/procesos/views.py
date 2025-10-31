from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from .models import ProcesoInterno, Proceso
from .forms import ProcesoInternoForm, ProcesoForm
from django.contrib.auth.decorators import login_required
from apps.usuarios.models import Usuario



@login_required
def index_proceso_interno(request):
    query = request.GET.get('q', '')
    if query:
        lista_procesos_internos = ProcesoInterno.objects.filter(
            titulo__icontains=query
        ).order_by('-fecha_registro')
    else:
        lista_procesos_internos = ProcesoInterno.objects.all().order_by('-fecha_registro')

    paginacion = Paginator(lista_procesos_internos, 6)
    numero_pagina = request.GET.get('page')
    pagina_actual = paginacion.get_page(numero_pagina)
    usuarios = Usuario.objects.exclude(rol__nombre="Cliente")

    context = {
        "banner_title": "Procesos Internos",
        "pagina_actual": pagina_actual,
        'usuarios': usuarios,
        "total_registros": lista_procesos_internos.count(),
        "query": query
    }
    return render(request, 'admin/procesos_internos/index.html', context=context)

@login_required
def registrar_proceso_interno(request):
    if request.method == 'POST':
        form = ProcesoInternoForm(request.POST)
        if form.is_valid():
            proceso_interno = form.save(commit=False)
            proceso_interno.save()
            form.save_m2m()  
            return redirect('procesos_internos')
        else:
            print(form.errors)
    else:
        form = ProcesoInternoForm()
    

    context = {
        'form': form, 
        'banner_title': 'Registrar Proceso Interno'
    }
    return render(request, 'admin/procesos_internos/index.html', context)

@login_required
def editar_proceso_interno(request, id_proceso_interno):
    proceso_interno = get_object_or_404(ProcesoInterno, id_proceso_interno=id_proceso_interno)

    if request.method == 'POST':
        form = ProcesoInternoForm(request.POST, instance=proceso_interno)
        if form.is_valid():
            proceso_interno = form.save(commit=False)
            proceso_interno.save()
            form.save_m2m()
            return redirect('procesos_internos')
        else:
            print(form.errors)
    else:
        form = ProcesoInternoForm(instance=proceso_interno)

    lista_procesos_internos = ProcesoInterno.objects.all().order_by('-fecha_registro')
    usuarios = Usuario.objects.exclude(rol__nombre="Cliente")

    context = {
        'form': form,
        'proceso_interno': proceso_interno,
        'pagina_actual': lista_procesos_internos,  # para el loop en el template
        'usuarios': usuarios,
        "total_registros": lista_procesos_internos.count(),
        "banner_title": "Procesos Internos"
    }
    return render(request, 'admin/procesos_internos/index.html', context)

@login_required
def eliminar_proceso_interno(request, id_proceso_interno):
    proceso_interno = get_object_or_404(ProcesoInterno, id_proceso_interno=id_proceso_interno)
    try:
        proceso_interno.delete()
    except Exception as e:
        print(f"Error al eliminar el proceso interno: {str(e)}")
    return redirect('procesos_internos')


@login_required
def index_proceso(request):
    query = request.GET.get('q', '')
    if query:
        lista_procesos = Proceso.objects.filter(
            titulo__icontains=query
        ).order_by('-fecha_solicitud')
    else:
        lista_procesos = Proceso.objects.all().order_by('-fecha_solicitud')

    paginacion = Paginator(lista_procesos, 6)
    numero_pagina = request.GET.get('page')
    pagina_actual = paginacion.get_page(numero_pagina)

    context = {
        "banner_title": "Procesos",
        "pagina_actual": pagina_actual,
        "total_registros": lista_procesos.count(),
        "query": query
    }
    return render(request, 'admin/procesos/index.html', context=context)

@login_required
def registrar_proceso(request):
    if request.method == 'POST':
        form = ProcesoForm(request.POST)
        if form.is_valid():
            proceso = form.save(commit=False)
            proceso.save()
            form.save_m2m()
            return redirect('procesos')
        else:
            print(form.errors)
    else:
        form = ProcesoForm()

    context = {
        'form': form,
        'banner_title': 'Registrar Proceso'
    }
    return render(request, 'admin/procesos/index.html', context)

@login_required
def editar_proceso(request, id_proceso):
    proceso = get_object_or_404(Proceso, id_proceso=id_proceso)

    if request.method == 'POST':
        form = ProcesoForm(request.POST, instance=proceso)
        if form.is_valid():
            proceso = form.save(commit=False)
            proceso.save()
            form.save_m2m()
            return redirect('procesos')
        else:
            print(form.errors)
    else:
        form = ProcesoForm(instance=proceso)

    context = {
        'form': form,
        'proceso': proceso,
    }
    return render(request, 'admin/procesos/index.html', context)

@login_required
def eliminar_proceso(request, id_proceso):
    proceso = get_object_or_404(Proceso, id_proceso=id_proceso)
    try:
        proceso.delete()
    except Exception as e:
        print(f"Error al eliminar el proceso: {str(e)}")
    return redirect('procesos')
