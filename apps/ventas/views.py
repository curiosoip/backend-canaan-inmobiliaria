from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Venta
from .forms import VentaForm
from apps.viviendas.models import Vivienda
from apps.usuarios.models import Usuario
from apps.servicios.models import Servicio
@login_required
def index(request):
    ventas_activo = Venta.objects.exclude(estado='CANCELADO')
    for venta in ventas_activo:
        if venta.saldo_restante <= 0:
            venta.estado = 'CANCELADO'
            venta.save(update_fields=['estado'])

    query = request.GET.get('q', '')
    if query:
        lista_ventas = Venta.objects.filter(
            Q(usuario__username__icontains=query) |
            Q(lote__nombre__icontains=query) |
            Q(vivienda__nombre__icontains=query) |
            Q(tipo_venta__icontains=query) |
            Q(estado__icontains=query)
        ).order_by('-fecha_venta')
    else:
        lista_ventas = Venta.objects.all().order_by('-fecha_venta')

    paginacion = Paginator(lista_ventas, 6)
    numero_pagina = request.GET.get('page')
    pagina_actual = paginacion.get_page(numero_pagina)

    clientes = Usuario.objects.filter(rol__nombre='Cliente')

    context = {
        "banner_title": "Ventas",
        "pagina_actual": pagina_actual,
        "total_registros": lista_ventas.count(),
        "viviendas":Vivienda.objects.all(),
        "servicios":Servicio.objects.all(),
        "usuarios": clientes,
        "query": query
    }

    return render(request, 'admin/ventas/index.html', context=context)


@login_required
def eliminar_venta(request, id_venta):
    venta = get_object_or_404(Venta, id_venta=id_venta)
    try:
        venta.delete()
        messages.success(request, f"Venta de '{venta.usuario.username}' eliminada correctamente.")
    except Exception as e:
        messages.error(request, f"No se pudo eliminar la venta: {str(e)}")
    
    return redirect('ventas')


@login_required
def registrar_venta(request):
    if request.method == 'POST':
        form = VentaForm(request.POST)
        if form.is_valid():
            venta = form.save(commit=False)  
            venta.save()  
            form.save_m2m()  
            messages.success(request, "Venta registrada correctamente.")
            return redirect('ventas')
        else:
            messages.error(request, f"Errores en el formulario: {form.errors}")
    else:
        form = VentaForm()

    context = {
        'form': form,
        'banner_title': 'Registrar Venta'
    }

    return render(request, 'admin/ventas/index.html', context)
