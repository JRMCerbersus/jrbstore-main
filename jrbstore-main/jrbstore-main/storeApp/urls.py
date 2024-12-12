#storeapp urls

from django.urls import path
from . import views
from storeApp.views import crearTarjeta, editarTarjeta, eliminarTarjeta, listarTarjetas, logout_user, crearProducto, crearCategoria, listarCategoria, listarProducto, editarCategoria, editarProducto, eliminarCategoria  ,eliminarProducto, Registrarse, ventas, agregar_al_carrito, carrito,eliminar_producto_carrito, procesar_pago, ventas


urlpatterns = [
    path('crearproducto/',crearProducto,name='crearproducto'),
    path('listaproducto/',listarProducto,name='listaproducto'),
    path('editarproducto/<str:codigo>',editarProducto,name='editarproducto'),
    path('eliminarproducto/<str:codigo>',eliminarProducto,name='eliminarproducto'),
    
    path('crearcategoria/',crearCategoria,name='crearcategoria'),
    path('listacategoria/',listarCategoria,name='listacategoria'),
    path('editarcategoria/<str:codigo>',editarCategoria,name='editarcategoria'),
    path('eliminarcategoria/<str:codigo>',eliminarCategoria,name='eliminarcategoria'),
    
    path('productos/', views.productos, name='productos'),
    path('carrito/', views.carrito, name='carrito'),
    path('registrarse/', Registrarse, name='registrarse'),  # URL para el registro
    path('logout/', views.logout_user, name='logout'),
    path('Ventas/', ventas, name='Ventas'),
    path('carrito/agregar/<str:codigo>', agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/eliminar/<str:codigo>', eliminar_producto_carrito, name='eliminar_producto_carrito'),
    path('carrito/pagar/', procesar_pago, name='procesar_pago'),    
    path('ventas/', ventas, name='ventas'),  # Asegúrate de usar el mismo nombre
    
    path('creartarjeta/', crearTarjeta, name='creartarjeta'),
    path('listartarjetas/', listarTarjetas, name='tarjetas'),
    path('editartarjeta/<str:codigo>/', editarTarjeta, name='editartarjeta'),
    path('eliminartarjeta/<str:codigo>/', eliminarTarjeta, name='eliminartarjeta'),




    


]
