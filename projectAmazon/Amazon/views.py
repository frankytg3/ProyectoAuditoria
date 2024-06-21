from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from Amazon.fomrs import UserRegistrationForm

# Create your views here.

def productos(request):

    return render(request, "amazon/productos.html")

class LoginView(View):
    def get(self, request):
        return render(request, 'amazon/signin.html')
    

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            return render(request, 'registration/register_done.html', {'new_user': new_user})
    else:
        form = UserRegistrationForm()
    return render(request, 'amazon/register.html', {'form': form})
