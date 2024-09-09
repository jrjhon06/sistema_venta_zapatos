from django.db import models
from productos.models import Presentacion
from django.contrib.auth.models import User


class Cliente(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombres = models.CharField(verbose_name="Nombres", max_length=50)
    apellidos = models.CharField(verbose_name="Apellidos", max_length=50)
    email = models.EmailField(verbose_name="Email", max_length=70)
    dni = models.CharField(verbose_name="DNI", max_length=8, null=True)
    celular = models.CharField(verbose_name="Celular", max_length=20, null=True)
    telefono = models.CharField(verbose_name="Teléfono", max_length=20, null=True)
    direccion = models.CharField(verbose_name="Dirección", max_length=200, null=True)
    fecha_nacimiento = models.DateField(verbose_name="Fecha de nacimiento", max_length=200, null=True)
    usuario = models.ForeignKey(User, on_delete=models.RESTRICT)
    # id, nombres, apellidos, dni(8), celular, telefono, email, direccion
    # fecha_nacimiento

    def __str__(self):
        return self.nombres + " " + self.apellidos

    class Meta:
        db_table = 'cliente'
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'


def generar_numero_pedido():
    numero = ''
    try:
        maximo = Pedido.objects.aggregate(models.Max('numero'))
        if maximo["numero__max"] is None:
            numero = '0000000001'
        else:
            numero = str(int(maximo["numero__max"]) + 1).zfill(10)
    except Exception as error:
        print(error)
        pass
    return numero


class Pedido(models.Model):
    numero = models.CharField(verbose_name="Número", max_length = 100)
    fecha = models.DateField(verbose_name="Fecha")
    total = models.DecimalField(verbose_name="Total", max_digits=9, decimal_places=2)
    direccion = models.CharField(verbose_name="Dirección", max_length = 200)
    observacion = models.CharField(verbose_name="Dirección", max_length = 500)
    cliente = models.ForeignKey(Cliente, on_delete=models.RESTRICT, verbose_name="Cliente", null=True)

    class Meta:
        db_table = 'pedido'
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'


    def save(self, *args, **kwargs):
        if self.id is None:
            self.numero = generar_numero_pedido()

        super(Pedido, self).save(*args, **kwargs)


class DetallePedido(models.Model):
    # cantidad, precio_unitario, presentacion(FK), pedido(FK)
    cantidad = models.PositiveSmallIntegerField(verbose_name="Cantidad")
    precio_unitario = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Precio unitario')
    presentacion = models.ForeignKey(Presentacion, on_delete=models.RESTRICT, verbose_name='Presentación')
    pedido = models.ForeignKey(Pedido, on_delete=models.RESTRICT, verbose_name='Pedido')

    class Meta:
        db_table = 'detalle_pedido'
        verbose_name = 'Detalle de pedido'
        verbose_name_plural = 'Detalles de pedidos'
