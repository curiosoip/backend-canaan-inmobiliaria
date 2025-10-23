from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login
from rest_framework.response import Response


def index(request):
    return render(request, 'index.html')

@api_view(['GET'])
def login_redirect(request):
    user = request.user
    if not user.is_authenticated:
        return Response({'error': 'Usuario no autenticado'}, status=401)
    
    login(request, user)  

    refresh = RefreshToken.for_user(user)
    return Response({
        'access': str(refresh.access_token),
        'refresh': str(refresh),
        'next': request.GET.get('next', '/perfil')
    })