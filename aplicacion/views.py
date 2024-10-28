from django.shortcuts import render, redirect, get_object_or_404
from .models import Examen, SolicitudExamen
from .forms import SeleccionarExamenForm, ExamenForm, UsuarioForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import Usuario
from django.contrib.auth.decorators import user_passes_test


# views.py
def is_admin(user):
    return user.is_staff


@login_required
@user_passes_test(is_admin)  
def lista_usuarios(request):
    usuarios = Usuario.objects.all()  # Obtiene todos los usuarios
    return render(request, 'lista_usuarios.html', {'usuarios': usuarios})

@login_required
@user_passes_test(is_admin) 
def editar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario actualizado correctamente.')
            return redirect('lista_usuarios')
    else:
        form = UsuarioForm(instance=usuario)
    return render(request, 'editar_usuario.html', {'form': form, 'usuario': usuario})

@login_required
@user_passes_test(is_admin) 
def eliminar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    if request.method == 'POST':
        usuario.delete()
        messages.success(request, 'Usuario eliminado correctamente.')
        return redirect('lista_usuarios')
    return render(request, 'eliminar_usuario.html', {'usuario': usuario})

def registrar_usuario(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        second_name = request.POST['second_name']
        email = request.POST['email']
        password = request.POST['password']
        numero_control = request.POST['numero_control']  # Captura el número de control

        user = Usuario.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=second_name,
            email=email,
            password=password,
            numero_control=numero_control  # Agrega el número de control al crear el usuario
        )
        messages.success(request, "Usuario creado con éxito.")
        return redirect('iniciar_sesion')

    return render(request, 'registrar_usuario.html')



def iniciar_sesion(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('seleccionar_examen')
        else:
            messages.error(request, 'Credenciales incorrectas. Intenta de nuevo.')

    return render(request, 'iniciar_sesion.html')

@login_required
def seleccionar_examen(request):
    examenes = Examen.objects.all()
    return render(request, 'seleccionar_examen.html', {'examenes': examenes})

@login_required
@user_passes_test(is_admin)
def agregar_examen(request):
    if request.method == 'POST':
        form = ExamenForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Examen agregado correctamente.')
            return redirect('lista_examenes')
    else:
        form = ExamenForm()
    return render(request, 'agregar_examen.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def index(request):
    return render(request, 'index.html')

@login_required
@user_passes_test(is_admin)
def reservar_examen(request, examen_id):
    examen = get_object_or_404(Examen, id=examen_id)
    if request.method == 'POST':
        # Aquí puedes manejar la lógica de la solicitud de examen
        solicitud = SolicitudExamen(usuario=request.user, examen=examen)
        solicitud.save()
        messages.success(request, 'Examen reservado correctamente.')
        return redirect('seleccionar_examen')
    return render(request, 'reservar_examen.html', {'examen': examen})

@login_required
@user_passes_test(is_admin)
def ver_solicitudes(request):
    solicitudes = SolicitudExamen.objects.filter(usuario=request.user)
    return render(request, 'ver_solicitudes.html', {'solicitudes': solicitudes})

@login_required
@user_passes_test(is_admin)
def eliminar_solicitud(request, solicitud_id):
    solicitud = get_object_or_404(SolicitudExamen, id=solicitud_id, usuario=request.user)
    solicitud.delete()
    messages.success(request, 'Solicitud de examen eliminada.')
    return redirect('ver_solicitudes')

@login_required
@user_passes_test(is_admin)
def editar_examen(request, examen_id):
    examen = get_object_or_404(Examen, id=examen_id)

    if request.method == 'POST':
        form = ExamenForm(request.POST, instance=examen)
        if form.is_valid():
            form.save()
            messages.success(request, 'Examen actualizado correctamente.')
            return redirect('lista_examenes')
    else:
        # Convertir la fecha y hora al formato requerido
        examen.fecha = examen.fecha.strftime('%Y-%m-%dT%H:%M')  
        form = ExamenForm(instance=examen)  # Inicializa el formulario con el examen existente

    return render(request, 'editar_examen.html', {'form': form, 'examen': examen})

@login_required
@user_passes_test(is_admin)
def eliminar_examen(request, examen_id):
    examen = get_object_or_404(Examen, id=examen_id)
    if request.method == 'POST':
        examen.delete()
        messages.success(request, 'Examen eliminado correctamente.')
        return redirect('lista_examenes')
    return render(request, 'eliminar_examen.html', {'examen': examen})

@login_required
@user_passes_test(is_admin)  
def lista_examenes(request):
    examenes = Examen.objects.all()  # Obtiene todos los exámenes
    return render(request, 'lista_examenes.html', {'examenes': examenes})