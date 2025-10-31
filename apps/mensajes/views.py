from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Mensaje
from .serializers import MensajeSerializer
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages



@api_view(['POST'])
def crear_mensaje(request):
    serializer = MensajeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Mensaje enviado correctamente'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@login_required
def index(request):
    query = request.GET.get('q', '')
    mensajes_qs = Mensaje.objects.all().order_by('-fecha_creacion')

    if query:
        mensajes_qs = mensajes_qs.filter(
            Q(nombre_completo__icontains=query) |
            Q(correo__icontains=query) |
            Q(numero_whatsapp__icontains=query) |
            Q(mensaje__icontains=query)
        )

    paginacion = Paginator(mensajes_qs, 6)
    pagina_actual = paginacion.get_page(request.GET.get('page'))

    context = {
        "banner_title": "Mensajes Recibidos",
        "pagina_actual": pagina_actual,
        "total_registros": mensajes_qs.count(),
        "query": query,
    }

    return render(request, 'admin/mensajes/index.html', context)


@login_required
def marcar_mensaje_leido(request, id_mensaje):
    mensaje = get_object_or_404(Mensaje, id=id_mensaje)

    if not mensaje.leido:
        mensaje.leido = True
        mensaje.save()
        messages.success(request, f"Mensaje de '{mensaje.nombre_completo}' marcado como leído.")

    return redirect('mensajes')

@login_required
def eliminar_mensaje(request, id_mensaje):
    mensaje = get_object_or_404(Mensaje, id=id_mensaje)
    try:
        mensaje.delete()
        messages.success(request, f"Mensaje de '{mensaje.nombre_completo}' eliminado correctamente.")
    except Exception as e:
        messages.error(request, f"No se pudo eliminar el mensaje: {str(e)}")

    return redirect('mensajes')