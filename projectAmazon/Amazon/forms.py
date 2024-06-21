from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from Amazon.models import Cliente
from datetime import date

def validate_age_range(value):
    min_age = 18
    max_age = 90
    if value:
        today = date.today()
        age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
        if age < min_age or age > max_age:
            raise ValidationError(f"La edad debe estar entre {min_age} y {max_age} años.")
        
def no_numeros_validator(value):
    if any(char.isdigit() for char in value):
        raise ValidationError('El campo no debe contener números')
    
def no_letras_validator(value):
    if any(char.isalpha() for char in value):
        raise ValidationError('El campo no debe contener letras')  

class formCliente(forms.Form):
    correo = forms.EmailField(label="Correo electrónico")  
    nombres=forms.CharField(max_length=30,validators=[no_numeros_validator])
    telefono=forms.CharField(max_length=9,validators=[no_letras_validator])
    fecha_Nacimiento=forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), validators=[validate_age_range])

    class Meta:
        model = Cliente
        fields = ['correo', 'nombres','telefono', 'fecha_Nacimiento']
    
    def clean_fecha_Nacimiento(self):
        fecha_nacimiento = self.cleaned_data.get('fecha_Nacimiento')
        validate_age_range(fecha_nacimiento)  # Llamar al validador personalizado para fecha de nacimiento
        return fecha_nacimiento
    