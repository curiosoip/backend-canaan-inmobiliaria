from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from django.contrib.auth import login
from .forms import UsuarioRegisterForm,RolForm,RolUpdateForm,UsuarioModalForm,UsuarioUpdateForm
from .models import Rol
from utils.storages.r2_storage import upload_to_r2
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from django.contrib import messages


from .models import Usuario

class UploadFotoUsuarioView(View):
    def post(self, request):
        file = request.FILES.get('file')
        if not file:
            return JsonResponse({'error': 'No se envió ningún archivo'}, status=400)

        foto_url = upload_to_r2(file, file.name, file.content_type)

        usuario = request.user
        usuario.foto_url = foto_url 
        usuario.save()

        return JsonResponse({'foto_url': foto_url})




def clientes(request):
    query = request.GET.get('q', '')

    usuarios_qs = Usuario.objects.filter(rol__nombre__iexact='cliente').order_by('-fecha_registro')

    if query:
        usuarios_qs = usuarios_qs.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(username__icontains=query)
        )

    paginacion = Paginator(usuarios_qs, 6)
    pagina_actual = paginacion.get_page(request.GET.get('page'))

    context = {
        "banner_title": "Usuarios - Clientes",
        "pagina_actual": pagina_actual,
        "total_registros": usuarios_qs.count(),
        "query": query,
        "grupo": "cliente",
        "roles": Rol.objects.all()
    }
    return render(request, 'admin/usuarios/index.html', context)


def empresas(request):
    query = request.GET.get('q', '')
    usuarios_qs = Usuario.objects.exclude(rol__nombre__iexact='cliente').order_by('-fecha_registro')
    if query:
        usuarios_qs = usuarios_qs.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(username__icontains=query)
        )
    paginacion = Paginator(usuarios_qs, 6)
    pagina_actual = paginacion.get_page(request.GET.get('page'))

    context = {
        "banner_title": "Usuarios - Empresas",
        "pagina_actual": pagina_actual,
        "total_registros": usuarios_qs.count(),
        "query": query,
        "grupo": "empresa",
        "roles": Rol.objects.all()
    }
    return render(request, 'admin/usuarios/index.html', context)

def eliminarusuario(request, id_usuario):
    usuario = get_object_or_404(Usuario, id_usuario=id_usuario)
    try:
        usuario.delete()
        messages.success(request, f"Usuario '{usuario.username}' eliminado correctamente.")
    except Exception as e:
        messages.error(request, f"No se pudo eliminar el usuario: {str(e)}")

    return redirect('usuarios')



def registrar_usuario(request):
    if request.method == 'POST':
        form = UsuarioModalForm(request.POST, request.FILES)  
        if form.is_valid():
            form.save()
            messages.success(request, "Usuario registrado correctamente.")
            return redirect('usuarios')
        else:
            for field, errores in form.errors.items():
                for error in errores:
                    messages.error(request, f"{field}: {error}")
            return redirect('usuarios')
    else:
        form = UsuarioModalForm()

    context = {
        'form': form,
        'banner_title': 'Crear Usuario',
        'roles': Rol.objects.all(), 
    }
    return render(request, 'admin/usuarios/index.html', context)

def editar_usuario(request, id_usuario):
    usuario = get_object_or_404(Usuario, id_usuario=id_usuario)
    if request.method == 'POST':
        form = UsuarioUpdateForm(request.POST, request.FILES, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, f"Usuario '{usuario.username}' actualizado correctamente.")
            return redirect('usuarios')
        else:
            for field, errores in form.errors.items():
                for error in errores:
                    messages.error(request, f"{field}: {error}")
            return redirect('usuarios')
    else:
        form = UsuarioUpdateForm(instance=usuario)
    
    context = {
        'form': form,
        'usuario': usuario,
        'roles': Rol.objects.all()
    }
    return render(request, 'admin/usuarios/editar.html', context)


def index_roles(request):
    roles_qs = Rol.objects.all().order_by('-fecha_registro')

    context = {
        "banner_title": "Roles",
        "roles": roles_qs,  
        "total_registros": roles_qs.count()
    }
    return render(request, 'admin/roles/index.html', context)




def registrar_rol(request):
    if request.method == 'POST':
        form = RolForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Rol creado correctamente.")
            return redirect('roles')
        else:
            for field, errores in form.errors.items():
                for error in errores:
                    messages.error(request, f"{field}: {error}")
            return redirect('roles')
    else:
        form = RolForm()

    context = {
        'form': form,
        'banner_title': 'Crear Rol'
    }
    return render(request, 'admin/roles/index.html', context)


def editar_rol(request, id_rol):
    rol = get_object_or_404(Rol, id_rol=id_rol)
    if request.method == 'POST':
        form = RolUpdateForm(request.POST, instance=rol)
        if form.is_valid():
            form.save()
            messages.success(request, f"Rol '{rol.nombre}' actualizado correctamente.")
            return redirect('roles')
        else:
            for field, errores in form.errors.items():
                for error in errores:
                    messages.error(request, f"{field}: {error}")
            return redirect('roles')
    else:
        form = RolUpdateForm(instance=rol)

    context = {
        'form': form,
        'rol': rol,
        'banner_title': 'Editar Rol'
    }
    return render(request, 'admin/roles/editar.html', context)


def eliminar_rol(request, id_rol):
    rol = get_object_or_404(Rol, id_rol=id_rol)
    try:
        rol.delete()
        messages.success(request, f"Rol '{rol.nombre}' eliminado correctamente.")
    except Exception as e:
        messages.error(request, f"No se pudo eliminar el rol: {str(e)}")
    return redirect('roles')