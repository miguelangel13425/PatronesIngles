import os
import sys

# Añade el directorio del proyecto al sistema de rutas
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Establece la configuración del proyecto
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'calendario.settings')

# Importa la aplicación WSGI de Django
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
