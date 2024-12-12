from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.core.exceptions import ValidationError
from storeApp.forms import ProductoForm, CategoriaForm, RegistroForm, TarjetaForm
from storeApp.models import Producto, Categoria, Tarjeta, Venta, Plataforma
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Count
from django.contrib.auth.decorators import login_required, permission_required
from axes.models import AccessAttempt
import traceback
import logging

def index(request):
    return render(request, 'index.html')
 
@permission_required('storeApp.add_producto',login_url='/')
def crearProducto(request):
    form = ProductoForm()
    data = {
        'titulo': 'Crear Producto',
        'formulario': form,
        'plataformas': Plataforma.objects.all()  # Obtener todas las plataformas
    }

    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)

        # Validar que se haya subido una foto
        if request.FILES.get('foto'):
            foto = request.FILES['foto']
            valid_extensions = ['.png', '.jpg', '.jpeg', '.webp']
            if not any(foto.name.endswith(ext) for ext in valid_extensions):
                return HttpResponseBadRequest("Formato de imagen no válido. Solo se permiten PNG, JPG y WEBP.")

        if form.is_valid():
            producto = form.save()  # Guardar el producto
            # Las plataformas seleccionadas se guardan automáticamente
            messages.success(request, 'Producto creado con éxito!')
            return redirect('crearproducto')  # Redirigir para evitar reenvíos de formulario
        else:
            print(form.errors)

    return render(request, 'storeApp/create.html', data)

@permission_required('storeApp.view_producto',login_url='/')
def listarProducto(request):
    productos  = Producto.objects.all()
    data = {'lista': productos}

    return render(request,'storeApp/producto.html', data)

from django.contrib import messages  # Asegúrate de que esto esté importado

@permission_required('storeApp.change_producto',login_url='/')
def editarProducto(request, codigo):
    prod = Producto.objects.get(pk=codigo)
    form = ProductoForm(instance=prod)

    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=prod)
        if form.is_valid():
            if request.FILES:
                if prod.foto:
                    # Capturar la foto antigua
                    prodAn = Producto.objects.get(pk=codigo)
                    prodAn.foto.delete()

            form.save()
            messages.success(request, 'Producto editado con éxito!')  # Establecer el mensaje aquí

    data = {
        'titulo': 'Editar Producto',
        'formulario': form,
        'foto_actual': prod.foto.url if prod.foto else None
    }
    return render(request, 'storeApp/create.html', data)

@permission_required('storeApp.delete_producto',login_url='/')
def eliminarProducto(request,codigo):
    prod = Producto.objects.get(pk=codigo)
    #verifica si el registro tiene foto
    if prod.foto:
        #si tiene foto la elimina
        prod.foto.delete()
    prod.delete()
    messages.success(request, 'Categoría eliminada con éxito!')
    return redirect('/listaproducto/')


@permission_required('storeApp.add_categoria',login_url='/')
def crearCategoria(request):
    form = CategoriaForm()
    data = {
        'titulo': 'Crear Categoria',
        'formulario': form,
        'messages': messages.get_messages(request)  # Asegúrate de incluir esto
    }

    if request.method == 'POST':
        form = CategoriaForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria creada con éxito! :D')
            return redirect('crearcategoria')  # Redirigir para evitar reenvíos de formulario
        else:
            print(form.errors)

    return render(request, 'categoria/create2.html', data)


@permission_required('storeApp.view_categoria',login_url='/')
def listarCategoria(request):
    categorias = Categoria.objects.all()
    data = {'lista': categorias}
    return render(request, 'categoria/categoria.html', data)


@permission_required('storeApp.change_categoria',login_url='/')
def editarCategoria(request, codigo):
    cat = Categoria.objects.get(pk=codigo)
    form = CategoriaForm(instance=cat)

    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=cat)

        if form.is_valid():
            form.save()
            messages.success(request,'la Categoria ha sido modificada con exito! :D')

    data = {
        'titulo':'Editar Categoria',
        'formulario':form
    }
    return render(request,'categoria/create2.html', data)


@permission_required('storeApp.delete_categoria ',login_url='/')
def eliminarCategoria(request, codigo):
    cat = get_object_or_404(Categoria, pk=codigo)
    cat.delete()
    messages.success(request, 'Categoría eliminada con éxito!')
    return redirect('listacategoria')



def Registrarse(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registrado con éxito! :D')
            return redirect('inicio') 
        else:
            for error in form.errors.values():
                messages.error(request, error)

    form = RegistroForm()  
    return render(request, 'registration/registro.html', {'formulario': form, 'titulo': 'Registro'})


# Configura logging
logger = logging.getLogger(__name__)

def login_user(request):
    try:
        if request.method == 'POST':
            form = AuthenticationForm(data=request.POST)
            username = request.POST.get('username')
            
            # Logging detallado
            logger.error(f"Intento de login para usuario: {username}")
            
            # Buscar intentos de acceso para este usuario
            attempts = AccessAttempt.objects.filter(username=username)
            
            # Debug de intentos
            logger.error(f"Número de intentos: {attempts.count()}")
            
            # Verificar si el usuario está bloqueado
            is_locked = False
            last_attempt = attempts.last()
            
            if last_attempt:
                is_locked = last_attempt.is_locked_out()
                logger.error(f"Último intento de bloqueo: {last_attempt}")
                logger.error(f"¿Está bloqueado?: {is_locked}")
                
                # Información adicional de bloqueo
                logger.error(f"Detalles de bloqueo: {last_attempt.__dict__}")
            
            if form.is_valid():
                # Intentar autenticar
                user = authenticate(
                    username=username, 
                    password=request.POST.get('password')
                )
                
                # Lógica de bloqueo más detallada
                if is_locked:
                    logger.error(f"BLOQUEO DETECTADO para {username}")
                    messages.error(request, "Tu cuenta está temporalmente bloqueada. Intenta de nuevo más tarde.")
                    return render(request, 'registration/login.html', {'form': form})
                
                # Si las credenciales son correctas y NO está bloqueado
                if user is not None:
                    login(request, user)
                    # Limpiar intentos fallidos al iniciar sesión correctamente
                    attempts.delete()
                    messages.success(request, f"¡Bienvenido {username}!")
                    return redirect('index')
                else:
                    # Credenciales incorrectas
                    logger.error(f"Credenciales incorrectas para {username}")
                    messages.error(request, "Usuario o contraseña incorrectos.")
            else:
                logger.error(f"Formulario inválido para {username}")
                messages.error(request, "Formulario inválido.")
        else:
            form = AuthenticationForm()
        
        return render(request, 'registration/login.html', {'form': form})
    
    except Exception as e:
        # Captura y registra cualquier excepción
        logger.error(f"Error en login_user: {str(e)}")
        logger.error(traceback.format_exc())
        messages.error(request, "Ocurrió un error inesperado.")
        return render(request, 'registration/login.html', {'form': AuthenticationForm()})

def logout_user(request):
    logout(request)  # Cierra la sesión del usuario
    messages.success(request, "Has cerrado sesión con éxito.")
    return redirect('inicio')  # Redirige al inicio u otra página
            



def productos(request):
    categoria_seleccionada = request.GET.get('categoria')  # Obtener la categoría seleccionada del filtro
    search_query = request.GET.get('search')  # Obtener la consulta de búsqueda
    categorias = Categoria.objects.all()  # Obtener todas las categorías
    
    if categoria_seleccionada:
        productos = Producto.objects.filter(categoria_id=categoria_seleccionada)  # Filtrar por categoría
    else:
        productos = Producto.objects.all()  # Mostrar todos los productos si no hay filtro

    if search_query:
        productos = productos.filter(nombre__icontains=search_query)  # Filtrar por nombre del producto
        mensaje_busqueda = f'Resultados de búsqueda para "{search_query}"'  # Mensaje de búsqueda
    else:
        mensaje_busqueda = None  # Sin mensaje si no hay búsqueda

    return render(request, 'storeApp/productos.html', {
        'productos': productos,
        'categorias': categorias,
        'categoria_seleccionada': int(categoria_seleccionada) if categoria_seleccionada else None,
        'mensaje_busqueda': mensaje_busqueda,  # Pasar el mensaje a la plantilla
    })

def agregar_al_carrito(request, codigo):
    producto = Producto.objects.get(codigoBarra=codigo)
    carrito = request.session.get('carrito', [])

    for item in carrito:
        if item['codigoBarra'] == producto.codigoBarra:
            item['cantidad'] += 1
            item['total'] = item['cantidad'] * item['precio']
            request.session['carrito'] = carrito
            return JsonResponse({'success': True, 'nombre': producto.nombre})

    carrito.append({
        'codigoBarra': producto.codigoBarra,
        'nombre': producto.nombre,
        'precio': producto.precio,
        'cantidad': 1,
        'total': producto.precio,
        'imagen_url': producto.foto.url
    })

    # Guardar el carrito actualizado en la sesión
    request.session['carrito'] = carrito
    return JsonResponse({'success': True, 'nombre': producto.nombre})
    return redirect('carrito')  # Redirige al carrito para mostrarlo
    return redirect('productos')  # Redirigir de vuelta a la lista de productos

def carrito(request):
    carrito = request.session.get('carrito', [])

    # Validar que el carrito sea una lista de diccionarios
    if not isinstance(carrito, list) or any(not isinstance(item, dict) for item in carrito):
        carrito = []  # Reinicia el carrito si está mal formateado
        request.session['carrito'] = carrito

    # Actualizar el total para cada producto en el carrito
    for item in carrito:
        # Asegurarse de que la cantidad no sea negativa
        if item['cantidad'] < 0:
            item['cantidad'] = 0  # Establece la cantidad a 0 si es negativa
        item['total'] = item['cantidad'] * item['precio']

    # Recalcular el total del carrito
    total = sum(item['total'] for item in carrito)

    return render(request, 'storeApp/carrito.html', {'carrito': carrito, 'total': total})

def eliminar_producto_carrito(request, codigo):
    carrito = request.session.get('carrito', [])
    print(carrito)  # Imprime el contenido del carrito
    producto_en_carrito = next((item for item in carrito if str(item['codigoBarra']) == str(codigo)), None)
    if producto_en_carrito:
        carrito = [item for item in carrito if str(item['codigoBarra']) != str(codigo)]
        request.session['carrito'] = carrito
    else:
        messages.error(request, 'El producto no existe en el carrito')
    return redirect('carrito')

def procesar_pago(request):
    if request.method == 'POST':
        carrito = request.session.get('carrito', [])
        usuario = request.user

        if not usuario.is_authenticated:
            messages.error(request, "Debes iniciar sesión para realizar la compra.")
            return redirect('login')

        if not carrito:
            messages.error(request, "El carrito está vacío.")
            return redirect('carrito')

        # Registrar cada producto en el carrito como una venta
        for item in carrito:
            # Obtener la cantidad actualizada desde el formulario
            cantidad = int(request.POST.get(f'cantidad_{item["codigoBarra"]}', item['cantidad']))
            total = cantidad * item['precio']  # Calcular el nuevo precio total

            Venta.objects.create(
                usuario=usuario,
                producto=Producto.objects.get(codigoBarra=item['codigoBarra']),
                cantidad=cantidad,
                precio_total=total
            )

        # Limpiar el carrito después del pago
        request.session['carrito'] = []

        messages.success(request, "Pago realizado con éxito. ¡Gracias por tu compra!")
        return redirect('productos')  # Redirigir a la página de ventas

    return redirect('carrito')



def ventas(request):
    if request.user.is_superuser:
        ventas = Venta.objects.select_related('producto').all()
    else:
        ventas = Venta.objects.select_related('producto').filter(usuario=request.user)

    # Agrupar las ventas por usuario y fecha
    ventas_agrupadas = {}
    for venta in ventas:
        key = (venta.usuario.id, venta.fecha)  # Agrupar por usuario y fecha
        if key not in ventas_agrupadas:
            ventas_agrupadas[key] = {
                'usuario': venta.usuario.username,  # Nombre del usuario
                'fecha': venta.fecha,
                'productos': [],
                'total_venta': 0  # Inicializar el total de la venta
            }

        # Agregar detalles del producto a la venta agrupada
        ventas_agrupadas[key]['productos'].append({
            'producto': venta.producto.nombre,
            'precio_unitario': venta.precio_total / venta.cantidad,
            'cantidad': venta.cantidad,
            'total': venta.precio_total  # Total de la venta
        })
        ventas_agrupadas[key]['total_venta'] += venta.precio_total  # Calcular el total de la venta

    # Convertir el diccionario a una lista para pasar a la plantilla
    ventas_agrupadas_list = [
        {
            'usuario': v['usuario'],
            'fecha': v['fecha'],
            'productos': v['productos'],
            'total_venta': v['total_venta'],
        }
        for v in ventas_agrupadas.values()
    ]

    return render(request, 'storeApp/ventas.html', {
        'ventas_agrupadas': ventas_agrupadas_list,
    })
    

@permission_required('storeApp.add_tarjeta', login_url='/')
def crearTarjeta(request):
    form = TarjetaForm()
    categorias = Categoria.objects.all()  # Obtener todas las categorías
    data = {
        'titulo': 'Crear Tarjeta',
        'formulario': form,
        'categorias': categorias, # Agrega esto

    }

    if request.method == 'POST':
        form = TarjetaForm(request.POST, request.FILES)

        # Validar que se haya subido una foto
        if request.FILES.get('foto'):
            foto = request.FILES['foto']
            valid_extensions = ['.png', '.jpg', '.jpeg', '.webp']
            if not any(foto.name.endswith(ext) for ext in valid_extensions):
                return HttpResponseBadRequest("Formato de imagen no válido. Solo se permiten PNG, JPG y WEBP.")

        if form.is_valid():
            form.save()  # Guardar la tarjeta
            messages.success(request, 'Tarjeta creada con éxito!')
            return redirect('tarjetas')  # Redirigir a la lista de tarjetas
        else:
            print(form.errors)

    return render(request, 'tarjetas/tarjetasCreator.html', data)

@permission_required('storeApp.view_tarjeta', login_url='/')
def listarTarjetas(request):
    tarjetas = Tarjeta.objects.all()
    data = {'lista': tarjetas}
    return render(request, 'tarjetas/tarjetas.html', data)

@permission_required('storeApp.change_tarjeta', login_url='/')
def editarTarjeta(request, codigo):
    tarjeta = get_object_or_404(Tarjeta, pk=codigo)
    form = TarjetaForm(instance=tarjeta)

    if request.method == 'POST':
        form = TarjetaForm(request.POST, request.FILES, instance=tarjeta)
        if form.is_valid():
            if request.FILES:
                if tarjeta.foto:
                    # Capturar la foto antigua
                    tarjeta.foto.delete()

            form.save()
            messages.success(request, 'Tarjeta editada con éxito!')
            return redirect('tarjetas')  # Redirigir a la lista de tarjetas

    data = {
        'titulo': 'Editar Tarjeta',
        'formulario': form,
        'foto_actual': tarjeta.foto.url if tarjeta.foto else None
    }
    return render(request, 'tarjetas/tarjetasCreator.html', data)

@permission_required('storeApp.delete_tarjeta', login_url='/')
def eliminarTarjeta(request, codigo):
    tarjeta = get_object_or_404(Tarjeta, pk=codigo)
    # Verifica si el registro tiene foto
    if tarjeta.foto:
        # Si tiene foto la elimina
        tarjeta.foto.delete()
    tarjeta.delete()
    messages.success(request, 'Tarjeta eliminada con éxito!')
    return redirect('tarjetas')  # Redirigir a la lista de tarjetas