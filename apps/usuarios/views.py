from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from ...utils.storages.r2_storage import upload_to_r2

class UploadFotoUsuarioView(View):
    def post(self, request):
        file = request.FILES.get('file')
        if not file:
            return JsonResponse({'error': 'No se envió ningún archivo'}, status=400)

        foto_url = upload_to_r2(file, file.name, file.content_type)

        usuario = request.user
        usuario.foto = foto_url
        usuario.save()

        return JsonResponse({'foto_url': foto_url})

