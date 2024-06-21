from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from Amazon.models import Cliente

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

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
    fecha_Nacimiento=forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Cliente
        fields = ['correo', 'nombres','telefono', 'fecha_Nacimiento']
    