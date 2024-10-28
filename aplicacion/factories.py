import factory
from factory import SubFactory
from faker import Faker
from django.utils import timezone
from datetime import timedelta
from .models import Usuario, Examen, SolicitudExamen

fake = Faker()

class UsuarioFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Usuario

    username = factory.LazyAttribute(lambda _: fake.user_name())
    email = factory.LazyAttribute(lambda _: fake.email())
    numero_control = factory.LazyAttribute(lambda _: fake.unique.random_number(digits=10, fix_len=True))
    password = factory.PostGenerationMethodCall('set_password', 'password123')  # Contraseña predefinida
    is_staff = factory.LazyAttribute(lambda _: fake.boolean(chance_of_getting_true=10))  # 10% de probabilidad de ser admin
    first_name = factory.LazyAttribute(lambda _: fake.first_name())
    last_name = factory.LazyAttribute(lambda _: fake.last_name())

class ExamenFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Examen

    fecha = factory.LazyAttribute(lambda _: timezone.now() + timedelta(weeks=1))  # Fecha una semana adelante
    cupo = factory.LazyAttribute(lambda _: fake.random_int(min=10, max=50))
    costo = factory.LazyAttribute(lambda _: fake.pydecimal(left_digits=4, right_digits=2, positive=True))

class SolicitudExamenFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SolicitudExamen

    usuario = SubFactory(UsuarioFactory)
    examen = SubFactory(ExamenFactory)
    estado_pago = factory.LazyAttribute(lambda _: fake.boolean(chance_of_getting_true=70))  # 70% probabilidad de pagado
    calificacion = factory.LazyAttribute(lambda _: fake.random_int(min=0, max=100))  # Calificación aleatoria entre 0-100
    fecha_solicitud = factory.LazyAttribute(lambda _: timezone.now())
