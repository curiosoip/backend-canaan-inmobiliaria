from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import Servicio
from .forms import ServicioForm
from django.contrib import messages


@login_required
def index(request):
    lista_servicios = Servicio.objects.all().order_by('-fecha_registro')

    context = {
        "banner_title": "Servicios",
        "servicios": lista_servicios,
        "total_registros": lista_servicios.count(),
    }
    return render(request, 'admin/servicios/index.html', context)


@login_required
def registrar_servicio(request):
    if request.method == 'POST':
        form = ServicioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Servicio registrado correctamente.")
            return redirect('servicios')
        else:
            # Mostrar errores al usuario
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = ServicioForm()

    context = {
        'form': form,
        'banner_title': 'Registrar Servicio'
    }
    return render(request, 'admin/servicios/index.html', context)


@login_required
def editar_servicio(request, id_servicio):
    servicio = get_object_or_404(Servicio, id_servicio=id_servicio)

    if request.method == 'POST':
        form = ServicioForm(request.POST, instance=servicio)
        if form.is_valid():
            form.save()
            messages.success(request, "Servicio actualizado correctamente.")
            return redirect('servicios')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = ServicioForm(instance=servicio)

    context = {
        'form': form,
        'servicio': servicio,
        'banner_title': 'Editar Servicio'
    }
    return render(request, 'admin/servicios/index.html', context)


@login_required
def eliminar_servicio(request, id_servicio):
    servicio = get_object_or_404(Servicio, id_servicio=id_servicio)
    try:
        servicio.delete()
        messages.success(request, "Servicio eliminado correctamente.")
    except Exception as e:
        messages.error(request, f"Error al eliminar el servicio: {str(e)}")
    return redirect('servicios')
