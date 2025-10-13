from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid

class Rol(models.Model):
    id_rol = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre
    
    class Meta:
        db_table = 'rol'
        verbose_name = "Rol"
        verbose_name_plural = "Roles"

class Usuario(AbstractUser):
    id_usuario = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    rol = models.ForeignKey(Rol, on_delete=models.SET_NULL, null=True, blank=True, related_name='usuarios',name="rol")
    celular=models.CharField(max_length=25,blank=True,null=True,name="celular")
    foto_url = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=False)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} ({self.rol})" if self.rol else self.username
    
    class Meta:
        db_table = 'usuario'
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
