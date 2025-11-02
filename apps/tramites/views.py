from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Tramite,Requisito
from .forms import TramiteForm,RequisitoForm
from django.core.paginator import Paginator
from django.db.models import Q
from apps.departamentos.models import Departamento

@login_required
def index_tramites(request):
    query = request.GET.get('q', '')

    tramites_qs = Tramite.objects.all().order_by('-fecha_registro')

    if query:
        tramites_qs = tramites_qs.filter(
            Q(nombre__icontains=query) |
            Q(descripcion__icontains=query)
        )

    paginacion = Paginator(tramites_qs, 6)
    pagina_actual = paginacion.get_page(request.GET.get('page'))

    context = {
        "banner_title": "Trámites",
        "pagina_actual": pagina_actual,
        "total_registros": tramites_qs.count(),
        "departamentos":Departamento.objects.all(),
        "query": query,
    }

    return render(request, 'admin/tramites/index.html', context)


@login_required
def registrar_tramite(request):
    if request.method == 'POST':
        form = TramiteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Trámite registrado correctamente.")
            return redirect('tramites')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = TramiteForm()

    context = {
        'form': form,
        'banner_title': 'Registrar Trámite'
    }
    return render(request, 'admin/tramites/index.html', context)


@login_required
def editar_tramite(request, id_tramite):
    tramite = get_object_or_404(Tramite, id_tramite=id_tramite)

    if request.method == 'POST':
        form = TramiteForm(request.POST, instance=tramite)
        if form.is_valid():
            form.save()
            messages.success(request, "Trámite actualizado correctamente.")
            return redirect('tramites')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = TramiteForm(instance=tramite)

    context = {
        'form': form,
        'tramite': tramite,
        'banner_title': 'Editar Trámite'
    }
    return render(request, 'admin/tramites/index.html', context)


@login_required
def eliminar_tramite(request, id_tramite):
    tramite = get_object_or_404(Tramite, id_tramite=id_tramite)
    try:
        tramite.delete()
        messages.success(request, "Trámite eliminado correctamente.")
    except Exception as e:
        messages.error(request, f"Error al eliminar el trámite: {str(e)}")
    return redirect('tramites')



@login_required
def index_requisitos(request):
    lista_requisitos = Requisito.objects.select_related('tramite').all().order_by('orden')

    context = {
        "banner_title": "Requisitos",
        "requisitos": lista_requisitos,
        "total_registros": lista_requisitos.count(),
    }
    return render(request, 'admin/tramites/index.html', context)


@login_required
def registrar_requisito(request, id_tramite):
    tramite = get_object_or_404(Tramite, id_tramite=id_tramite)

    if request.method == 'POST':
        form = RequisitoForm(request.POST)
        if form.is_valid():
            requisito = form.save(commit=False)
            requisito.tramite = tramite
            requisito.save()
            messages.success(request, "Requisito registrado correctamente.")
            return redirect('tramites') 
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = RequisitoForm()

    context = {
        'form': form,
        'tramite': tramite,
        'banner_title': f'Registrar Requisito para {tramite.nombre}',
    }
    return render(request, 'admin/tramites/index.html', context)



@login_required
def eliminar_requisito(request, id_requisito_tramite):
    requisito = get_object_or_404(Requisito, id_requisito_tramite=id_requisito_tramite)
    try:
        requisito.delete()
        messages.success(request, "Requisito eliminado correctamente.")
    except Exception as e:
        messages.error(request, f"Error al eliminar el requisito: {str(e)}")
    return redirect('requisitos')