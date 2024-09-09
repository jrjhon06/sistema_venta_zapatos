from django.db import models
from configuracion.models import Color, Medida
from autoslug import AutoSlugField

# productos_categoria


class Categoria(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    tipo_categoria = models.CharField(
        max_length=30, null=True, blank=True, verbose_name='Tipo de categoría')
    descripcion = models.CharField(max_length=100, verbose_name='Descripción')

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'categoria'
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'


class Marca(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=50, verbose_name="Nombre")

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'marca'
        verbose_name = 'Marca'
        verbose_name_plural = 'Marcas'


class Producto(models.Model):
    id = models.BigAutoField(primary_key=True)
    titulo = models.CharField(verbose_name="Título", max_length=150)
    precio = models.DecimalField(
        verbose_name="Precio", max_digits=9, decimal_places=2)
    descripcion = models.TextField(
        verbose_name="Descripción", null=True, blank=True)
    activo = models.BooleanField(verbose_name="¿Activo?", default=True)
    # llaves foranes
    # marca_id
    marca = models.ForeignKey(
        Marca, on_delete=models.RESTRICT, verbose_name="Marca")
    # categoria_id
    categoria = models.ForeignKey(
        Categoria, on_delete=models.RESTRICT, verbose_name='Categoría')
    slug = AutoSlugField(populate_from="titulo", unique=["titulo"], always_update=True, null=True)
    # representar las relaciones de muchos a muchos
    # colores
    colores = models.ManyToManyField(Color, through='presentacion')
    medidas = models.ManyToManyField(Medida, through='presentacion')


    # zapatillas 2024 -> zapatillas-2024
    # zapatillas 2024 -> zapatillas-2024-1
    # zapatillas 2024 -> zapatillas-2024-2
    # zapatillas version 2024 -> zapatillas-version-2024

    def __str__(self):
        return self.titulo
    

    def primeras_imagenes(self):
        return self.imagenproducto_set.order_by('orden')[:2]

    class Meta:
        db_table = 'producto'
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'


class Presentacion(models.Model):
    id = models.BigAutoField(primary_key=True)
    stock = models.DecimalField(
        verbose_name="Stock", max_digits=9, decimal_places=2)
    producto = models.ForeignKey(
        Producto, on_delete=models.RESTRICT, verbose_name="Producto")
    medida = models.ForeignKey(
        Medida, on_delete=models.RESTRICT,  verbose_name="Medida")
    color = models.ForeignKey(
        Color, on_delete=models.RESTRICT,  verbose_name="Color")

    # ABC - S - BLANCO
    def __str__(self):
        return self.producto.titulo + ' - ' + self.medida.nombre + ' - ' + self.color.nombre

    class Meta:
        db_table = 'presentacion'
        verbose_name = 'Presentación de producto'
        verbose_name_plural = 'Presentaciones de productos'


class ImagenProducto(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.ImageField(max_length=200, verbose_name="Nombre", upload_to="productos")
    orden = models.PositiveSmallIntegerField(verbose_name="Orden")
    producto = models.ForeignKey(Producto, on_delete=models.RESTRICT, verbose_name="Producto")


    def __str__(self):
        return self.producto.titulo + ': Imagen ' + str(self.orden)
    

    class Meta:
        db_table = 'imagen_producto'
        verbose_name = 'Imagen de producto'
        verbose_name_plural = 'Imagenes de productos'
