from django.shortcuts import render
from django.contrib.auth import login
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login,get_user_model
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

User = get_user_model()

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
        elif request.user.rol:
            return redirect('usuarios_empresas')
        else:
            messages.error(request, "Tu cuenta no tiene un rol asignado.")
            return redirect('login')

    if request.method == 'POST':
        username_or_email = request.POST.get('username')
        password = request.POST.get('password')

        user = None

        try:
            validate_email(username_or_email)
            is_email = True
        except ValidationError:
            is_email = False

        if is_email:
            try:
                user_obj = User.objects.get(email=username_or_email)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None
        else:
            user = authenticate(request, username=username_or_email, password=password)

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
            elif user.rol and user.rol.nombre != 'Administrador' and user.rol.nombre != 'Cliente':
                return redirect('usuarios_empresas')
            else:
                messages.warning(request, "Tu cuenta no tiene un rol asignado.")
                return redirect('login')
        else:
            messages.error(request, "Nombre de usuario o contraseña incorrectos.")
            return render(request, 'login.html')

    return render(request, 'login.html')