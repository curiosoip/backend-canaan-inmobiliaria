from django.shortcuts import render
from django.db.models import Count
from django.db.models.functions import ExtractWeek
from django.db.models import F
from django.db.models.functions import Extract
from datetime import datetime, timedelta  # Añadir timedelta aquí
from django.db.models.functions import TruncDate
import json
from apps.servicios.models import Servicio

def index(request):
    servicios_activos = Servicio.objects.filter(activo=True)
    
    return render(request, 'admin/reportes/index.html', {
        'servicios_activos': servicios_activos
    })

