from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import  UserCreationForm
from Amazon.models import Cliente
from django.contrib import messages
from django.db import IntegrityError
from Amazon.forms import formCliente

# Create your views here.

def productos(request):

    return render(request, "amazon/productos.html")

class LoginView(View):
    def get(self, request):
        return render(request, 'amazon/signin.html')
    

def register(request):
    if request.method == "POST":
        formcli = formCliente(request.POST, request.FILES)
        formRegister = UserCreationForm(request.POST)
        if formcli.is_valid() and formRegister.is_valid():
            try:
                correo = formcli.cleaned_data['correo']
                user = formRegister.save(commit=False)  # Guardar usuario
                user.email = correo  # Establecer el correo electrónico del usuario
                user.save()

                Cliente.objects.create(
                    user=user,
                    nombres=formcli.cleaned_data['nombres'],
                    telefono=formcli.cleaned_data['telefono'],
                    fecha_Nacimiento=formcli.cleaned_data['fecha_Nacimiento'],

                )
                messages.success(request, 'Usuario registrado exitosamente. Por favor inicia sesión.')
                return render(request, 'Amazon/register_done.html', {'new_user': user})
            except IntegrityError:
                messages.error(request, 'Error: El nombre de usuario ya está en uso.')
    else:
        formcli = formCliente()
        formRegister = UserCreationForm()
    
    return render(request, "amazon/register.html", {
        'formUser': formRegister,
        'formCliente': formcli,
    })