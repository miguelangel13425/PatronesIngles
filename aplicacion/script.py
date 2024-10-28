import os
import sys
import django
from faker import Faker
from django.core.management import call_command
from django.db import transaction
from django.contrib.auth.hashers import make_password

# Configura Django antes de importar modelos
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aplicacion.settings')  # Ajusta esto según el nombre de tu archivo settings.py
sys.path.append(os.path.dirname(__file__))  # Agrega la ruta del directorio actual
django.setup()

from .models import Usuario, Examen, SolicitudExamen  # Mueve las importaciones aquí
from .factories import UsuarioFactory, ExamenFactory

fake = Faker()

# El resto del código permanece igual...


# Borra todos los datos de la base de datos
def clear_database():
    call_command('flush', '--no-input')

# Crear un nuevo administrador
def create_admin():
    admin = Usuario.objects.create(
        first_name='Admin',
        last_name='Admin',
        email='admin@gmail.com',
        username='admin',
        password=make_password('admin'),  # Hash de la contraseña
        is_staff=True,
        is_superuser=True
    )
    admin.save()
    print("Administrador creado con éxito.")

# Crea usuarios
def create_users():
    for _ in range(300):  # Crear 300 usuarios
        UsuarioFactory()

# Crea exámenes
def create_exams():
    for _ in range(200):  # Crear 200 exámenes
        ExamenFactory()

# Crea solicitudes de examen
def create_exam_requests():
    users = Usuario.objects.all()
    exams = Examen.objects.all()

    if not users.exists() or not exams.exists():
        print("No hay usuarios o exámenes disponibles para crear solicitudes.")
        return

    for _ in range(500):  # Crear 800 solicitudes
        user = fake.random_element(users)
        exam = fake.random_element(exams)
        
        # Verifica si la solicitud ya existe
        if not SolicitudExamen.objects.filter(usuario=user, examen=exam).exists():
            SolicitudExamen.objects.create(
                usuario=user,
                examen=exam,
                estado_pago=fake.boolean(),
                calificacion=fake.random_int(min=0, max=100),
            )
        else:
            print(f"La solicitud para el usuario {user} y el examen {exam} ya existe.")


# Ejecuta el script
def populate_database():
    clear_database()
    create_admin()  # Asegúrate de que se crea el administrador
    create_users()
    create_exams()
    create_exam_requests()

if __name__ == '__main__':
    with transaction.atomic():
        populate_database()
