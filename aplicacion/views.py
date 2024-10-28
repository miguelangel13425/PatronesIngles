from django.shortcuts import render, redirect, get_object_or_404
from .models import Examen, SolicitudExamen
from .forms import SeleccionarExamenForm, ExamenForm, UsuarioForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import Usuario
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator
from django.db.models import Q
from .forms import SolicitudExamenForm  # Asegúrate de importar tu formulario


# views.py
def is_admin(user):
    return user.is_staff


@login_required
@user_passes_test(is_admin)  
def lista_usuarios(request):
    query = request.GET.get('search', '')  # Obtener el término de búsqueda
    usuarios = Usuario.objects.all()

    # Filtrar los usuarios basados en el término de búsqueda
    if query:
        usuarios = usuarios.filter(
            Q(first_name__icontains=query) |  # Ajusta esto según tu modelo
            Q(last_name__icontains=query) |    # Ajusta esto según tu modelo
            Q(numero_control__startswith=query) |  # Cambiado a startswith para número de control
            Q(email__icontains=query)              # Búsqueda por correo electrónico

        ).distinct()

    # Paginación
    paginator = Paginator(usuarios, 50)  # 50 usuarios por página
    page_number = request.GET.get('page')  # Obtener el número de página de la URL
    usuarios_page = paginator.get_page(page_number)

    return render(request, 'lista_usuarios.html', {'usuarios': usuarios_page, 'search': query})

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
    # Obtener todos los exámenes
    examenes = Examen.objects.all()

    # Filtrar los exámenes que el usuario ya ha solicitado
    examenes_disponibles = examenes.exclude(
        id__in=SolicitudExamen.objects.filter(usuario=request.user).values_list('examen_id', flat=True)
    )

    if request.method == 'POST':
        examen_id = request.POST.get('examen_id')
        examen = Examen.objects.get(id=examen_id)
        
        # Crear la solicitud de examen
        SolicitudExamen.objects.create(
            usuario=request.user,
            examen=examen,
            estado_pago=False,  # Por defecto no está pagado
            calificacion=0      # Por defecto la calificación es 0
        )
        
        messages.success(request, 'Solicitud de examen creada correctamente.')
        return redirect('seleccionar_examen')  # Redirigir a la misma página o a donde desees

    return render(request, 'seleccionar_examen.html', {'examenes': examenes_disponibles})

@login_required
def solicitudes_vinculadas(request):
    # Filtrar los exámenes por el usuario actual
    solicitudes = SolicitudExamen.objects.filter(usuario=request.user)
    return render(request, 'solicitudes_vinculadas.html', {'solicitudes': solicitudes})

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
    query = request.GET.get('search', '')  # Obtener el término de búsqueda
    estado_pago = request.GET.get('estado_pago', '')  # Obtener el estado de pago

    solicitudes = SolicitudExamen.objects.all()

    # Filtrar las solicitudes basadas en el término de búsqueda
    if query:
        solicitudes = solicitudes.filter(
            Q(usuario__first_name__icontains=query) | 
            Q(usuario__last_name__icontains=query) | 
            Q(usuario__numero_control__startswith=query) | 
            Q(calificacion__icontains=query)
        ).distinct()

    # Filtrar por estado de pago
    if estado_pago in ['True', 'False']:
        estado_pago_bool = estado_pago == 'True'
        solicitudes = solicitudes.filter(estado_pago=estado_pago_bool)

    # Paginación
    paginator = Paginator(solicitudes, 50)  # 50 solicitudes por página
    page_number = request.GET.get('page')  # Obtener el número de página de la URL
    solicitudes_page = paginator.get_page(page_number)

    return render(request, 'ver_solicitudes.html', {'solicitudes': solicitudes_page, 'search': query, 'estado_pago': estado_pago})


@login_required
@user_passes_test(is_admin)
def agregar_solicitud(request):
    if request.method == 'POST':
        form = SolicitudExamenForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Solicitud de examen agregada correctamente.')
            return redirect('lista_solicitudes')
    else:
        form = SolicitudExamenForm()
    return render(request, 'agregar_solicitud.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def editar_solicitud(request, solicitud_id):
    solicitud = get_object_or_404(SolicitudExamen, id=solicitud_id)

    if request.method == 'POST':
        form = SolicitudExamenForm(request.POST, instance=solicitud)  # Usa el formulario aquí
        if form.is_valid():
            form.save()
            messages.success(request, 'Solicitud de examen actualizada correctamente.')
            return redirect('ver_solicitudes')
    else:
        form = SolicitudExamenForm(instance=solicitud)  # Inicializa el formulario con la solicitud existente

    return render(request, 'editar_solicitud.html', {'form': form, 'solicitud': solicitud})

@login_required
@user_passes_test(is_admin)
def eliminar_solicitud(request, solicitud_id):
    solicitud = get_object_or_404(SolicitudExamen, id=solicitud_id)
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
    query = request.GET.get('search', '')  # Obtener el término de búsqueda
    examenes = Examen.objects.all()  # Obtiene todos los exámenes

    # Filtrar los exámenes basados en el término de búsqueda
    if query:
        examenes = examenes.filter(
            Q(fecha__icontains=query)   # Ajusta esto según tu modelo (si es que tienes alguna descripción)
        ).distinct()

    # Paginación
    paginator = Paginator(examenes, 50)  # 50 exámenes por página
    page_number = request.GET.get('page')  # Obtener el número de página de la URL
    examenes_page = paginator.get_page(page_number)

    return render(request, 'lista_examenes.html', {'examenes': examenes_page, 'search': query})