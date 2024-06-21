from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cliente')
    nombres = models.CharField(max_length=100)
    telefono = models.CharField(max_length=9)  
    fecha_Nacimiento = models.DateField()

    def __str__(self):
        return self.nombres
