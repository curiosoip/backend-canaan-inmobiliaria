from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from .models import Usuario, Rol

@receiver(user_signed_up)
def set_cliente_rol(request, user, **kwargs):
    if isinstance(user, Usuario):
        cliente_rol = Rol.objects.filter(nombre__iexact='Cliente').first()
        if cliente_rol:
            user.rol = cliente_rol
        user.set_unusable_password()
        user.save()
