from django.shortcuts import render
from django.contrib.auth import login
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages


def index(request):
    return render(request, 'login.html')

def panel(request):
    return render(request, 'admin/_base.html')



def login_view(request):
    if request.user.is_authenticated:
        if request.user.rol and request.user.rol.nombre == 'Administrador':
            return redirect('usuarios_empresas')
        elif request.user.rol and request.user.rol.nombre == 'Cliente':
            messages.error(request, "No tienes acceso a este administrador.")
            return redirect('login')
        else:
            messages.warning(request, "Tu cuenta no tiene un rol asignado.")
            return redirect('login')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if not user.is_active:
                messages.error(request, "Tu cuenta está inactiva. Contacta con el administrador.")
                return redirect('login')

            login(request, user)

            if user.rol and user.rol.nombre == 'Administrador':
                return redirect('usuarios_empresas')
            elif user.rol and user.rol.nombre == 'Cliente':
                messages.error(request, "No tienes acceso a este administrador.")
                return redirect('login')
            else:
                messages.warning(request, "Tu cuenta no tiene un rol asignado.")
                return redirect('login')
        else:
            messages.error(request, "Nombre de usuario o contraseña incorrectos.")
            return render(request, 'login.html')

    return render(request, 'login.html')