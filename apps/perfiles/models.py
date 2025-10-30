from django.db import models
from django.conf import settings
from apps.tramites.models import Requisito
from apps.ventas.models import Venta
from apps.cuotas.models import Cuota
from apps.pagos.models import Pago
from apps.usuarios.models import Usuario
import uuid

class Perfil(models.Model):
    id_perfil = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='perfil')
    direccion = models.CharField(max_length=250, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    foto_perfil_url = models.URLField(blank=True, null=True)
    documentos = models.ManyToManyField(Requisito, through='DocumentoUsuario', blank=True)

    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Perfil de {self.usuario.first_name} {self.usuario.last_name}"

    def ventas(self):
        return Venta.objects.filter(usuario=self.usuario)

    def pagos(self):
        return Pago.objects.filter(usuario=self.usuario)

    def cuotas(self):
        return Cuota.objects.filter(venta__usuario=self.usuario)

    def documentos_subidos(self):
        return self.documentos_usuario.all()




class DocumentoUsuario(models.Model):
    id_documento = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='documentos_usuario')
    requisito = models.ForeignKey(Requisito, on_delete=models.CASCADE,blank=True,null=True)
    archivo_url = models.URLField()
    fecha_subida = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Documento de Usuario"
        verbose_name_plural = "Documentos de Usuario"
        ordering = ['fecha_subida']

    def __str__(self):
        return f"{self.requisito.nombre} - {self.perfil.usuario.username}"

