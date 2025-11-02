from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Consultoria
from .forms import ConsultoriaForm
from django.db.models import Q


@login_required
def index_consultorias(request):
    query = request.GET.get('q', '')

    consultorias_qs = Consultoria.objects.all().order_by('-fecha_registro')

    if query:
        consultorias_qs = consultorias_qs.filter(
            Q(titulo__icontains=query) |
            Q(descripcion__icontains=query)
        )

    paginacion = Paginator(consultorias_qs, 6)  
    pagina_actual = paginacion.get_page(request.GET.get('page'))

    context = {
        "banner_title": "Consultorías",
        "pagina_actual": pagina_actual,
        "total_registros": consultorias_qs.count(),
        "query": query,
    }

    return render(request, 'admin/consultorias/index.html', context)

@login_required
def registrar_consultoria(request):
    if request.method == 'POST':
        form = ConsultoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Consultoría registrada correctamente.")
            return redirect('consultorias')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = ConsultoriaForm()

    context = {
        'form': form,
        'banner_title': 'Registrar Consultoría'
    }
    return render(request, 'admin/consultorias/index.html', context)

@login_required
def editar_consultoria(request, id_consultoria):
    consultoria = get_object_or_404(Consultoria, id=id_consultoria)

    if request.method == 'POST':
        form = ConsultoriaForm(request.POST, instance=consultoria)
        if form.is_valid():
            form.save()
            messages.success(request, "Consultoría actualizada correctamente.")
            return redirect('consultorias')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = ConsultoriaForm(instance=consultoria)

    context = {
        'form': form,
        'consultoria': consultoria,
        'banner_title': 'Editar Consultoría'
    }
    return render(request, 'admin/consultorias/index.html', context)

@login_required
def eliminar_consultoria(request, id_consultoria):
    consultoria = get_object_or_404(Consultoria, id=id_consultoria)
    try:
        consultoria.delete()
        messages.success(request, "Consultoría eliminada correctamente.")
    except Exception as e:
        messages.error(request, f"Error al eliminar la consultoría: {str(e)}")
    return redirect('consultorias')
