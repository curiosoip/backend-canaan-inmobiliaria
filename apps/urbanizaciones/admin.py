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
import ocrmypdf
import tempfile
import os
from pdf2image import convert_from_bytes
from rapidocr import RapidOCR
from asgiref.sync import async_to_sync
import math



logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

ocr = RapidOCR()

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

    async def extract_text_cloudflare(self, result) -> dict:
      
        hermes_payload = {
            "messages": [
                {
                    "role": "system",
                    "content": "Devuelve solo un JSON con total_manzanas, total_lotes, area_total y las vértices con este_x y norte_y."
                },
                {
                    "role": "user",
                    "content": f"Extrae los datos del siguiente texto:\n\n{result}"
                }
            ],
            "response_format": {
                "type": "json_schema",
                "json_schema": {
                    "type": "object",
                    "properties": {
                        "total_manzanas": {"type": "integer"},
                        "total_lotes": {"type": "integer"},
                        "area_total": {"type": "number"},
                        "vertices": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "este_x": {"type": "number"},
                                    "norte_y": {"type": "number"}
                                },
                                "required": ["este_x", "norte_y"]
                            }
                        }
                    },
                    "required": ["total_manzanas", "total_lotes", "area_total", "vertices"]
                }
            },
            "raw": True,
            "max_tokens": 256,
            "temperature": 0
        }



        async with httpx.AsyncClient(timeout=httpx.Timeout(120.0)) as client:
            hermes_resp = await client.post(
                f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/ai/run/@cf/ibm-granite/granite-4.0-h-micro",
                headers={"Authorization": f"Bearer {AUTH_TOKEN}"},
                json=hermes_payload
            )

        if hermes_resp.status_code != 200:
            logger.warning("Hermes-2 API returned %s: %s", hermes_resp.status_code, hermes_resp.text)
            return {}

        data_resumen = hermes_resp.json()


        print(f"\n===== RESULTADO=====\n{data_resumen}\n============================\n")


        return {
            "data": data_resumen.get("result", {})
        }



    def save(self, commit=True):
        instance = super().save(commit=False)

        # Guardar portada
        portada_file = self.cleaned_data.get("portada_file")
        if portada_file:
            instance.portada_url = upload_to_r2(
                portada_file,
                filename=f"urbanizacion_portada_{instance.id_urbanizacion or 'temp'}_{portada_file.name}",
                content_type=portada_file.content_type
            )

        if commit:
            instance.save()

        planimetria_file = self.cleaned_data.get("planimetria_file")
        if not planimetria_file:
            return instance

        try:
            pdf_bytes = planimetria_file.read()

            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_in:
                temp_in.write(pdf_bytes)
                input_path = temp_in.name

            output_path = tempfile.NamedTemporaryFile(delete=False, suffix="_ocr.pdf").name

            ocrmypdf.ocr(
                input_path,
                output_path,
                language="spa",
                force_ocr=True,
                rotate_pages=False,  # no gira páginas
                deskew=False,        # no corrige inclinación
                output_type="pdf"
            )

            with open(output_path, "rb") as f:
                ocr_pdf_bytes = f.read()

            pages = convert_from_bytes(ocr_pdf_bytes, dpi=150)

            all_text = ""
            for i, page in enumerate(pages, start=1):
                image_path = f"temp_page_{i}.png"
                page.save(image_path, "PNG")
                
                result = ocr(image_path)
                
                page_text = str(result.txts)
                all_text += page_text + "\n"
                
                print(f"Página {i}/{len(pages)} procesada (OCR)")

            print("\n===== TEXTO COMPLETO DEL PDF OCR =====\n")
            print(all_text)
            print("\n====================================\n")
            resultado = async_to_sync(self.extract_text_cloudflare)(all_text)
            print(resultado)

            instance.planimetria_pdf = upload_to_r2(
                BytesIO(ocr_pdf_bytes),
                filename=f"urbanizacion_planimetria_ocr_{instance.id_urbanizacion}_{planimetria_file.name}",
                content_type="application/pdf"
            )

            logger.info("✅ PDF OCR generado y subido correctamente: %s", instance.planimetria_pdf)
            instance.save()

        except Exception as e:
            logger.error("❌ Error al procesar OCR del PDF: %s", e)

        finally:
            # Limpieza de archivos temporales
            for path in [locals().get("input_path"), locals().get("output_path")]:
                if path and os.path.exists(path):
                    try:
                        os.remove(path)
                    except Exception:
                        pass

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
