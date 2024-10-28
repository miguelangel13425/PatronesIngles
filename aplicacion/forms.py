from django import forms
from .models import Examen, SolicitudExamen  # Importamos los modelos
from .models import Usuario
from datetime import datetime


class SolicitudExamenForm(forms.ModelForm):
    class Meta:
        model = SolicitudExamen
        fields = ['usuario', 'examen', 'estado_pago', 'calificacion']
        
        widgets = {
            'calificacion': forms.NumberInput(attrs={'min': 0, 'max': 100}),  # Validar calificación
        }


class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['numero_control','username', 'first_name', 'last_name', 'is_active']  # Agrega los campos que necesites


class CrearUsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # Establecemos la contraseña de forma segura
        if commit:
            user.save()
        return user


class SeleccionarExamenForm(forms.ModelForm):
    class Meta:
        model = SolicitudExamen  # Asocia este formulario con el modelo SolicitudExamen
        fields = ['examen']  # Solo mostramos el campo de selección de examen
        widgets = {
            'examen': forms.Select(),  # Widget de selección para el examen
        }


class ExamenForm(forms.ModelForm):
    class Meta:
        model = Examen
        fields = ['fecha', 'cupo', 'costo']
        widgets = {
            'fecha': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
    