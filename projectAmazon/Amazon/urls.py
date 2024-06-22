from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *

urlpatterns = [
    
    path('',productos,name='productos'),
    path('login/', iniciarsecion, name='login'),
    path('register/', register, name='register'),
    path('logout/', cerrarSecion, name='logout'),
    path('productos/<int:id>/', detalle_producto, name='detalle_producto'),
    path('masProductos',todos_los_productos,name='todo_los_productos'),
    path('productos/<int:id>/agregar-al-carrito/', agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/', ver_carrito, name='ver_carrito'),
    path('carrito/actualizar/<int:id>/', actualizar_cantidad, name='actualizar_cantidad'),
    path('direccion-y-carrito/', direccion_y_carrito, name='direccion_y_carrito'),
    path('metodo_pago/', metodo_de_pago, name='metodo_de_pago'),
    path('pago-realizado/', pago_realizado, name='pago_realizado'),
    
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)