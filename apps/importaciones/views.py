from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Importacion
from .forms import ImportacionForm
from django.db.models import Q

@login_required
def index_importaciones(request):
    query = request.GET.get('q', '')

    importaciones_qs = Importacion.objects.all().order_by('-fecha_registro')

    if query:
        importaciones_qs = importaciones_qs.filter(
            Q(nombre__icontains=query) |
            Q(servicios_asociados__icontains=query) |
            Q(proveedores__icontains=query)
        )

    paginacion = Paginator(importaciones_qs, 6)
    pagina_actual = paginacion.get_page(request.GET.get('page'))

    context = {
        "banner_title": "Importaciones",
        "pagina_actual": pagina_actual,
        "total_registros": importaciones_qs.count(),
        "query": query,
    }

    return render(request, 'admin/importaciones/index.html', context)

@login_required
def registrar_importacion(request):
    if request.method == 'POST':
        form = ImportacionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Importación registrada correctamente.")
            return redirect('importaciones')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = ImportacionForm()

    context = {
        'form': form,
        'banner_title': 'Registrar Importación'
    }
    return render(request, 'admin/importaciones/index.html', context)

@login_required
def editar_importacion(request, id_importacion):
    importacion = get_object_or_404(Importacion, id=id_importacion)

    if request.method == 'POST':
        form = ImportacionForm(request.POST, instance=importacion)
        if form.is_valid():
            form.save()
            messages.success(request, "Importación actualizada correctamente.")
            return redirect('importaciones')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = ImportacionForm(instance=importacion)

    context = {
        'form': form,
        'importacion': importacion,
        'banner_title': 'Editar Importación'
    }
    return render(request, 'admin/importaciones/index.html', context)

@login_required
def eliminar_importacion(request, id_importacion):
    importacion = get_object_or_404(Importacion, id=id_importacion)
    try:
        importacion.delete()
        messages.success(request, "Importación eliminada correctamente.")
    except Exception as e:
        messages.error(request, f"Error al eliminar la importación: {str(e)}")
    return redirect('importaciones')
