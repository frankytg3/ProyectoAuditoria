from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.forms import  UserCreationForm, AuthenticationForm
from Amazon.models import Cliente, Producto, Carrito, ItemCarrito, DireccionEnvio, Pago
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.db import IntegrityError
from Amazon.forms import formCliente, DireccionEnvioForm, PagoForm
from django.contrib.auth.decorators import login_required
from decimal import Decimal


# Create your views here.
   
def iniciarsecion(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('productos')
        else:
            return render(request, 'amazon/signin.html', {
                'formLogin': form,
            })
    else:
        form = AuthenticationForm()
        return render(request, 'amazon/signin.html', {
            'formLogin': form
        })
    
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
                    sexo=formcli.cleaned_data['sexo'],

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

def cerrarSecion(request):
    logout(request)
    return redirect('productos')

def productos(request):
    productos_list = Producto.objects.all()
    return render(request, "amazon/productos.html", {'productos': productos_list})

def todos_los_productos(request):
    productos_list = Producto.objects.all().order_by('?')  # Orden aleatorio
    return render(request, "amazon/total_productos.html", {'productos': productos_list})

def detalle_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    return render(request, 'amazon/detalle_producto.html', {'producto': producto})

@login_required
def agregar_al_carrito(request, id):
    producto = get_object_or_404(Producto, id=id)
    cantidad = int(request.POST.get('cantidad', 1))
    print(cantidad)
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)

    item, created = ItemCarrito.objects.get_or_create(carrito=carrito, producto=producto)
    
    item.cantidad = cantidad

    print(item.cantidad)
    item.save()

    messages.success(request, f'{producto.nombre} se ha agregado al carrito.')
    return redirect('ver_carrito')

@login_required
def ver_carrito(request):
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    items = ItemCarrito.objects.filter(carrito=carrito)
    total = sum(item.subtotal() for item in items)
    return render(request, 'amazon/carrito.html', {'items': items, 'total': total})

@login_required
def actualizar_cantidad(request, id):
    item = get_object_or_404(ItemCarrito, id=id, carrito__usuario=request.user)
    cantidad = int(request.POST.get('cantidad', item.cantidad))
    if cantidad > 0:
        item.cantidad = cantidad
        item.save()
    else:
        item.delete()
    return redirect('ver_carrito')

@login_required
def direccion_y_carrito(request):
    items = ItemCarrito.objects.all()  # Obtener todos los ítems del carrito
    total_parcial = 0
    for item in items:
        # Calcular el subtotal de cada ítem
        subtotal = item.producto.precio * item.cantidad
        item.subtotal = subtotal
        total_parcial += subtotal
    
    iva = total_parcial * Decimal('0.05')  # Calcular el IVA
    total_con_iva = total_parcial + iva  # Calcular el total con IVA

    user = request.user
    direccion_envio = DireccionEnvio.objects.filter(user=user).first()  # Obtener la dirección de envío existente, si la hay

    if request.method == 'POST':
        form = DireccionEnvioForm(request.POST, instance=direccion_envio)  # Pasar la instancia existente al formulario
        if form.is_valid():
            direccion = form.save(commit=False)  # Guardar la dirección de envío (crea o actualiza)
            direccion.user = user
            direccion.save()
            messages.success(request, 'Dirección guardada correctamente.')
            return redirect('direccion_y_carrito')  # Redirigir a la misma vista para refrescar el contexto
        else:
            messages.error(request, 'Por favor corrige los errores del formulario.')
    else:
        form = DireccionEnvioForm(instance=direccion_envio)  # Inicializar el formulario con la instancia existente

    context = {
        'form': form,
        'items': items,
        'total_parcial': total_parcial,
        'iva': iva,
        'total_con_iva': total_con_iva,
        'formularioEnviado': direccion_envio is not None,  # Verificar si hay dirección de envío guardada
    }
    
    return render(request, 'amazon/direccion_y_carrito.html', context)

@login_required
def metodo_de_pago(request):
    # Obtener todos los ítems del carrito
    items_carrito = ItemCarrito.objects.all()
    
    # Calcular el total a pagar incluyendo el IVA
    total_parcial = 0
    for item in items_carrito:
        subtotal = item.producto.precio * item.cantidad
        total_parcial += subtotal
    
    iva = total_parcial * Decimal('0.05')  # Calcular el IVA
    total_con_iva = total_parcial + iva  # Calcular el total con IVA

    metodo_pago = None  # Inicializar metodo_pago fuera del bloque POST

    if request.method == 'POST':
        metodo_pago = request.POST.get('metodo_pago')
        form = PagoForm(request.POST)
        if form.is_valid():
            # Procesar los datos del formulario
            Pago.objects.create(
                numero_tarjeta=form.cleaned_data['numero_tarjeta'],
                fecha_expiracion=form.cleaned_data['fecha_expiracion'],
                nombre_propietario=form.cleaned_data['nombre_propietario'],
                cvv=form.cleaned_data['cvv'],
                guardar_tarjeta=form.cleaned_data['guardar_tarjeta'],
            )

            # Lógica adicional según sea necesario, como guardar la tarjeta

            # Redirigir al usuario a la página de pago realizado
            return redirect('pago_realizado')
    else:
        form = PagoForm()
        

    context = {
        'total_a_pagar': total_con_iva,
        'form': form,
    }

    if metodo_pago == 'yape':
        # Lógica para el método de pago con YAPE
        monto_a_cobrar = total_con_iva
        context.update({
            'metodo_pago': 'YAPE',
            'monto_a_cobrar': monto_a_cobrar,
        })
    elif metodo_pago == 'tarjeta':
        # Lógica para el método de pago con tarjeta
        context.update({
            'metodo_pago': 'Tarjeta de Crédito',
        })
    elif request.method == 'POST':
        messages.error(request, 'Selecciona un método de pago válido.')

    return render(request, 'amazon/metodo_de_pago.html', context)

@login_required
def pago_realizado(request):
    # Obtener el carrito del usuario actual
    carrito_usuario = Carrito.objects.get(usuario=request.user)

    # Obtener todos los ítems del carrito del usuario actual
    items_carrito = ItemCarrito.objects.filter(carrito=carrito_usuario)

    # Eliminar todos los ítems del carrito
    items_carrito.delete()
    return render(request, 'amazon/pago_realizado.html')