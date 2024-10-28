from django.urls import path
from django.contrib import admin
from .views import (
    iniciar_sesion,
    seleccionar_examen,
    index,
    agregar_examen,
    reservar_examen,
    registrar_usuario,
    lista_usuarios,
    editar_usuario,
    eliminar_usuario,
    editar_examen,
    eliminar_examen,
    lista_examenes,
    ver_solicitudes,
    agregar_solicitud,
    eliminar_solicitud,
    editar_solicitud,
    solicitudes_vinculadas
)
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('iniciar_sesion/', iniciar_sesion, name='iniciar_sesion'),  
    path('', lista_examenes, name='index'),
    path('seleccionar_examen/', seleccionar_examen, name='seleccionar_examen'),  
    path('agregar_examen/', agregar_examen, name='agregar_examen'),  
    path('logout/', LogoutView.as_view(next_page='iniciar_sesion'), name='logout'),
    path('admin/', admin.site.urls),  
    path('reservar_examen/<int:examen_id>/', reservar_examen, name='reservar_examen'),
    path('registrar_usuario/', registrar_usuario, name='registrar_usuario'),
    path('lista_usuarios/', lista_usuarios, name='lista_usuarios'),  # Agrega la URL
    path('editar_usuario/<int:usuario_id>/', editar_usuario, name='editar_usuario'),  # Ruta para editar
    path('eliminar_usuario/<int:usuario_id>/', eliminar_usuario, name='eliminar_usuario'),  # Ruta para eliminar
    path('editar_examen/<int:examen_id>/', editar_examen, name='editar_examen'),
    path('eliminar_examen/<int:examen_id>/', eliminar_examen, name='eliminar_examen'),
    path('lista_examenes/', lista_examenes, name='lista_examenes'),
    path('ver_solicitudes/', ver_solicitudes, name='ver_solicitudes'),
    path('editar_solicitud/<int:solicitud_id>/', editar_solicitud, name='editar_solicitud'),
    path('agregar_solicitud/', agregar_solicitud, name='agregar_solicitud'),
    path('eliminar_solicitud/<int:solicitud_id>/', eliminar_solicitud, name='eliminar_solicitud'),
    path('solicitudes_vinculadas', solicitudes_vinculadas, name='solicitudes_vinculadas'),

]
