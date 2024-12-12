from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Plataforma(models.Model):
    nombre = models.CharField(max_length=50)
    icono = models.CharField(max_length=50)  # Almacena el nombre de la clase del icono

    def __str__(self):
        return self.nombre


class Categoria(models.Model):
    categoria = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.categoria}'

    class Meta:
        db_table = 'categoria'

class Producto(models.Model):
    codigoBarra = models.BigIntegerField(primary_key=True)
    nombre = models.CharField(max_length=50)
    categoria = models.ForeignKey(Categoria, null=False, on_delete=models.CASCADE)
    precio = models.PositiveIntegerField()
    stock = models.IntegerField()
    descripcion = models.TextField(max_length=300)
    foto = models.FileField(upload_to='productos')
    plataformas = models.ManyToManyField(Plataforma, blank=True)  # Relación de muchos a muchos, no obligatorio

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'producto'

class Registro(models.Model):
    nombre = models.CharField(max_length=50)
    email = models.EmailField(null=False, unique=True)
    contraseña = models.CharField(max_length=128)  # Longitud típica para contraseñas

    def __str__(self):
        return f'{self.nombre}'

    class Meta:
        db_table = 'Registro'

class Venta(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Usuario que realizó la compra
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)  # Producto comprado
    cantidad = models.PositiveIntegerField()  # Cantidad comprada
    precio_total = models.DecimalField(max_digits=10, decimal_places=2)  # Precio total
    fecha = models.DateTimeField(auto_now_add=True)  # Fecha de la venta

    def __str__(self):
        return f"Venta {self.id} - {self.usuario.username}"
    
class Tarjeta(models.Model):
    codigoBarra = models.BigIntegerField(primary_key=True)
    nombre = models.CharField(max_length=50)
    categoria = models.CharField(max_length=50)  # Ej. Steam, Xbox, PlayStation
    precio = models.PositiveIntegerField()
    stock = models.IntegerField()
    descripcion = models.TextField(max_length=300)
    foto = models.FileField(upload_to='tarjetas')

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'tarjeta'
