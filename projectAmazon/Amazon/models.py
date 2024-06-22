from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from .choices import sexos

# Create your models here.

class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cliente')
    nombres = models.CharField(max_length=100)
    telefono = models.CharField(max_length=9)  
    fecha_Nacimiento = models.DateField()
    sexo=models.CharField(max_length=1, choices=sexos, default='-')

    def __str__(self):
        return self.nombres

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    marca = models.CharField(max_length=100)
    color = models.CharField(max_length=50)
    material = models.CharField(max_length=100)
    tamaño = models.CharField(max_length=50)
    cantidad = models.PositiveIntegerField()
    imagen = models.ImageField(upload_to='productos/')

    def __str__(self):
        return self.nombre
    
class Carrito(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Carrito de {self.usuario.username}"

class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.cantidad * self.producto.precio

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"

class DireccionEnvio(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=9)
    direccion = models.CharField(max_length=255)
    estado = models.CharField(max_length=100)
    codigo_postal = models.CharField(max_length=5)
    fecha_creacion = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.nombre

class Cupon(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    descuento = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.codigo
    
class Pago(models.Model):
    numero_tarjeta = models.CharField(max_length=16)
    fecha_expiracion = models.CharField(max_length=5)
    nombre_propietario = models.CharField(max_length=100)
    cvv = models.CharField(max_length=4)
    guardar_tarjeta = models.BooleanField(default=False)
    fecha_pago = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pago realizado por {self.nombre_propietario} el {self.fecha_pago}"