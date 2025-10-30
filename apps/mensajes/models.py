# models.py
from django.db import models

class Mensaje(models.Model):
    nombre_completo = models.CharField(max_length=200)
    numero_whatsapp = models.CharField(max_length=20)
    correo = models.EmailField()
    mensaje = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    leido = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nombre_completo} - {self.correo}"

    class Meta:
        verbose_name = "Mensaje"
        verbose_name_plural = "Mensajes"
        ordering = ['-fecha_creacion']
