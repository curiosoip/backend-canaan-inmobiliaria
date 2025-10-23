# utils/logs.py
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.contenttypes.models import ContentType

def registrar_log(usuario, objeto, accion, mensaje=""):
    if not usuario or usuario.is_anonymous:
        return

    LogEntry.objects.log_action(
        user_id=usuario.pk,
        content_type_id=ContentType.objects.get_for_model(objeto).pk,
        object_id=objeto.pk,
        object_repr=str(objeto),
        action_flag=accion,
        change_message=mensaje,
    )
