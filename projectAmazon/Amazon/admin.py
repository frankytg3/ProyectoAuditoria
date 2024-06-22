from django.contrib import admin
from .models import Cliente, Producto
# Register your models here.

class clienteAdmin(admin.ModelAdmin):
    list_display=("user","nombres","telefono","fecha_Nacimiento")

admin.site.register(Cliente, clienteAdmin)

class productosAdmin(admin.ModelAdmin):
    list_display=(
        "nombre",
        "descripcion",
        "precio",
        "marca",
        "color",
        "material",
        "tamaño",
        "cantidad",
        "imagen"
        )

admin.site.register(Producto, productosAdmin)