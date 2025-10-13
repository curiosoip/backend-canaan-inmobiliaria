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

class UrbanizacionAdminForm(forms.ModelForm):
    portada_file = forms.FileField(required=False, label="Portada")
    planimetria_file = forms.FileField(required=False, label="Planimetría PDF")

    class Meta:
        model = Urbanizacion
        fields = "__all__"

    async def extract_text_from_image_cloudflare(self, image_bytes: bytes) -> str:
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")
        data_uri = f"data:image/jpeg;base64,{image_base64}"

        llama_payload = {
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "Eres un extractor experto de datos tabulares en documentos técnicos, planos o planimetrías.Extrae la información de la tabla CUADRO RESUMEN, Exactamente el total de manzanas,total de lotes y area total. "
                    )
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {"url": data_uri}
                        }
                    ]
                }
            ]
        }
        llama_payload_vertices = {
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "Eres un extractor experto de datos tabulares en documentos técnicos, planos o planimetrías.Extrae la información de la tabla SISTEMA DE REFERENCIA, Exactamente todos sus vértices, este x y norte y. "
                    )
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {"url": data_uri}
                        }
                    ]
                }
            ]
        }


        async with httpx.AsyncClient(timeout=None) as client:
            llama_resp = await client.post(
                f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/ai/run/@cf/meta/llama-4-scout-17b-16e-instruct",
                headers={"Authorization": f"Bearer {AUTH_TOKEN}"},
                json=llama_payload
            )

        if llama_resp.status_code != 200:
            logger.warning("Cloudflare API returned %s: %s", llama_resp.status_code, llama_resp.text)
            return ""

        extracted_text = llama_resp.json()
        print(f"\n===== RESPUESTA LLAMA-4 SCOUT =====\n{extracted_text}\n============================\n")




        hermes_payload = {
            "messages": [
                {
                    "role": "system",
                    "content": "Devuelve solo un JSON con total_manzanas, total_lotes y area_total."
                },
                {
                    "role": "user",
                    "content": f"Extrae los totales del siguiente texto:\n\n{extracted_text}"
                }
            ],
            "response_format": {
                "type": "json_schema",
                "json_schema": {
                    "type": "object",
                    "properties": {
                        "total_manzanas": {"type": "integer"},
                        "total_lotes": {"type": "integer"},
                        "area_total": {"type": "number"}
                    },
                    "required": ["total_manzanas", "total_lotes", "area_total"]
                }
            },
            "raw": True,
            "max_tokens": 256,
            "temperature": 0
        }

        async with httpx.AsyncClient(timeout=None) as client:
            hermes_resp = await client.post(
                f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/ai/run/@hf/nousresearch/hermes-2-pro-mistral-7b",
                headers={"Authorization": f"Bearer {AUTH_TOKEN}"},
                json=hermes_payload
            )

        if hermes_resp.status_code != 200:
            logger.warning("Hermes-2 API returned %s: %s", hermes_resp.status_code, hermes_resp.text)
            return {}

        data_resumen = hermes_resp.json()

        async with httpx.AsyncClient(timeout=None) as client:
            vertices_resp = await client.post(
                f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/ai/run/@cf/meta/llama-4-scout-17b-16e-instruct",
                headers={"Authorization": f"Bearer {AUTH_TOKEN}"},
                json=llama_payload_vertices
            )

        if vertices_resp.status_code != 200:
            logger.warning("Cloudflare API returned %s: %s", vertices_resp.status_code, vertices_resp.text)
            return ""

        extracted_text_vertices = vertices_resp.json()
        print(f"\n===== RESPUESTA VERTICES=====\n{extracted_text_vertices}\n============================\n")

        hermes_payload_vertices = {
            "messages": [
                {
                    "role": "system",
                    "content": "Devuelve solo un JSON con todos los vértices, cada uno con orden, este_x y norte_y."
                },
                {
                    "role": "user",
                    "content": f"Extrae los vértices con sus coordenadas del siguiente texto:\n\n{extracted_text_vertices}"
                }
            ],
            "response_format": {
                "type": "json_schema",
                "json_schema": {
                    "type": "object",
                    "properties": {
                        "vertices": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "orden": {"type": "string"},
                                    "este_x": {"type": "number"},
                                    "norte_y": {"type": "number"}
                                },
                                "required": ["orden", "este_x", "norte_y"]
                            }
                        }
                    },
                    "required": ["vertices"]
                }
            },
            "raw": True,
            "max_tokens": 512,
            "temperature": 0
        }

        async with httpx.AsyncClient(timeout=None) as client:
            hermes_resp_vertices = await client.post(
                f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/ai/run/@hf/nousresearch/hermes-2-pro-mistral-7b",
                headers={"Authorization": f"Bearer {AUTH_TOKEN}"},
                json=hermes_payload_vertices
            )

        if hermes_resp_vertices.status_code != 200:
            logger.warning("Hermes-2 API returned %s: %s", hermes_resp_vertices.status_code, hermes_resp_vertices.text)
            return {}

        data_vertices = hermes_resp_vertices.json()
        print(f"\n===== RESPUESTA VERTICES=====\n{data_vertices}\n============================\n")


        return {
            "resumen": data_resumen.get("result", {}),
            "vertices": data_vertices.get("result", {}).get("response", [])
        }



    def save(self, commit=True):
        instance = super().save(commit=False)

        # Guardar portada
        portada_file = self.cleaned_data.get("portada_file")
        if portada_file:
            instance.portada_url = upload_to_r2(
                portada_file,
                filename=f"urbanizacion_portada_{instance.id_urbanizacion}_{portada_file.name}",
                content_type=portada_file.content_type
            )

        if commit:
            instance.save()

        # Guardar planimetría y extraer datos
        planimetria_file = self.cleaned_data.get("planimetria_file")
        if planimetria_file:
            instance.planimetria_pdf = upload_to_r2(
                planimetria_file,
                filename=f"urbanizacion_planimetria_{instance.id_urbanizacion}_{planimetria_file.name}",
                content_type=planimetria_file.content_type
            )

            try:
                planimetria_file.seek(0)
                pdf_bytes = planimetria_file.read()
                images = convert_from_bytes(pdf_bytes, dpi=150)

                max_width = 1200
                for i, page_image in enumerate(images):
                    if page_image.width > max_width:
                        ratio = max_width / page_image.width
                        page_image = page_image.resize(
                            (max_width, int(page_image.height * ratio)),
                            resample=Image.Resampling.LANCZOS
                        )

                    image_bytes_io = BytesIO()
                    page_image.save(image_bytes_io, format="JPEG", quality=70)
                    image_bytes = image_bytes_io.getvalue()

                    # Aquí obtenemos el diccionario limpio
                    extracted_data = async_to_sync(self.extract_text_from_image_cloudflare)(image_bytes)
                    print(f"=== Datos extraídos página {i+1} ===\n{extracted_data}\n")

                    if isinstance(extracted_data, dict):
                        resumen = extracted_data.get("resumen", {}).get("response", {})
                        instance.total_manzanas = resumen.get("total_manzanas", 0)
                        instance.total_lotes = resumen.get("total_lotes", 0)
                        instance.area_total = resumen.get("area_total", 0.0)

                        instance.save()

                        # Guardar vértices
                        vertices = extracted_data.get("vertices", {}).get("vertices", []) or []


                        for v in vertices:
                            VerticeUrbanizacion.objects.update_or_create(
                                urbanizacion=instance,
                                orden=v.get("orden"),
                                defaults={
                                    "este_x": v.get("este_x"),
                                    "norte_y": v.get("norte_y")
                                }
                            )

            except Exception as e:
                logger.error("Error al procesar PDF: %s", e)

        return instance





@admin.register(Urbanizacion)
class UrbanizacionAdmin(admin.ModelAdmin):
    form = UrbanizacionAdminForm
    list_display = ('nombre', 'miniatura_portada', 'ver_planimetria','total_manzanas','total_lotes','area_total', 'departamento', 'fecha_registro')
    search_fields = ('nombre', 'departamento__nombre')
    list_filter = ('departamento',)
    readonly_fields = (
        'fecha_registro', 'fecha_actualizacion',
        'portada_url', 'planimetria_pdf',
        'miniatura_portada', 'ver_planimetria'
    )
    inlines = [VerticeUrbanizacionInline,LoteInline]

    fieldsets = (
        ('Información General', {
            'fields': ('nombre', 'descripcion', 'portada_url', 'portada_file',
                       'miniatura_portada', 'direccion', 'departamento')
        }),
        ('Ubicación', {'fields': ('latitude', 'longitude')}),
        ('Documentos', {'fields': ('planimetria_pdf', 'planimetria_file', 'ver_planimetria')}),
        ('Estadísticas', {'fields': ('total_manzanas','total_lotes', 'area_total')}),
        ('Tiempos de Registro', {
            'fields': ('fecha_registro', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )

    def miniatura_portada(self, obj):
        if obj.portada_url:
            return format_html(
                '<img src="{}" style="width: 80px; height: auto; border-radius: 8px;" />',
                obj.portada_url
            )
        return "-"
    miniatura_portada.short_description = "Portada"

    def ver_planimetria(self, obj):
        if obj.planimetria_pdf:
            return format_html(
                '<a href="{}" target="_blank" title="Ver Planimetría">'
                '<img src="https://cdn-icons-png.flaticon.com/512/337/337946.png" '
                'width="28" height="28" alt="PDF icon"/></a>', obj.planimetria_pdf
            )
        return "-"
    ver_planimetria.short_description = "Planimetría"

    def total_lotes(self, obj):
        return obj.lotes.count()
    total_lotes.short_description = "Total de Lotes"
