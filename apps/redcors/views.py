# apps/redcors/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import RedCORS
from .forms import RedCORSForm
from django.db.models import Q

@login_required
def index_redcors(request):
    query = request.GET.get('q', '')

    redcors_qs = RedCORS.objects.all().order_by('-fecha_registro')

    if query:
        redcors_qs = redcors_qs.filter(
            Q(nombre_proyecto__icontains=query) |
            Q(tipo_servicio__icontains=query) |
            Q(proveedor__icontains=query)
        )

    paginacion = Paginator(redcors_qs, 6)
    pagina_actual = paginacion.get_page(request.GET.get('page'))

    context = {
        "banner_title": "Red CORS",
        "pagina_actual": pagina_actual,
        "total_registros": redcors_qs.count(),
        "query": query,
    }

    return render(request, 'admin/redcors/index.html', context)


@login_required
def registrar_redcors(request):
    if request.method == 'POST':
        form = RedCORSForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Red CORS registrada correctamente.")
            return redirect('redcors')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = RedCORSForm()

    context = {
        'form': form,
        'banner_title': 'Registrar Red CORS'
    }
    return render(request, 'admin/redcors/index.html', context)


@login_required
def editar_redcors(request, id_redcors):
    redcors = get_object_or_404(RedCORS, id_redcors=id_redcors)

    if request.method == 'POST':
        form = RedCORSForm(request.POST, instance=redcors)
        if form.is_valid():
            form.save()
            messages.success(request, "Red CORS actualizada correctamente.")
            return redirect('redcors')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = RedCORSForm(instance=redcors)

    context = {
        'form': form,
        'redcors': redcors,
        'banner_title': 'Editar Red CORS'
    }
    return render(request, 'admin/redcors/index.html', context)


@login_required
def eliminar_redcors(request, id_redcors):
    redcors = get_object_or_404(RedCORS, id=id_redcors)
    try:
        redcors.delete()
        messages.success(request, "Red CORS eliminada correctamente.")
    except Exception as e:
        messages.error(request, f"Error al eliminar la Red CORS: {str(e)}")
    return redirect('redcors')
