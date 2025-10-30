import logging
from io import BytesIO
from django import forms
from django.contrib import admin
from django.utils.html import format_html
from asgiref.sync import async_to_sync
import httpx
import base64
from pdf2image import convert_from_bytes
from PIL import Image
from .models import Urbanizacion, Lote,VerticeUrbanizacion
from utils.storages.r2_storage import upload_to_r2

from pdf2image import convert_from_bytes
from asgiref.sync import async_to_sync
import math



logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


ACCOUNT_ID = "dea18ceb8496cd48c6b923cf46ee24dc"
AUTH_TOKEN = "eLzmD70pn8AXh7JPT2i7YMHEYuRV9IhlidAaFCpS"



class LoteInline(admin.TabularInline):
    model = Lote
    extra = 0
    fields = ('nombre', 'area_m2', 'precio', 'comprador', 'estado','manzana',
              'fecha_registro', 'fecha_actualizacion')
    readonly_fields = ('fecha_registro', 'fecha_actualizacion')
    ordering = ('nombre',)

class VerticeUrbanizacionInline(admin.TabularInline):
    model = VerticeUrbanizacion
    extra = 0
    fields = ('orden', 'este_x', 'norte_y', 'fecha_registro', 'fecha_actualizacion')
    readonly_fields = ('fecha_registro', 'fecha_actualizacion')
    ordering = ('orden',)
    verbose_name = "Vértice"
    verbose_name_plural = "Vértices"


