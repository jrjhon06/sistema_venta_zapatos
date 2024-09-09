from django.db import models
from productos.models import Presentacion
from django.utils import timezone
from compras.validators import validar_ruc


class Proveedor(models.Model):
    id = models.BigAutoField(primary_key=True)
    ruc = models.CharField(max_length=11, verbose_name='RUC', validators=[validar_ruc])
    razon_social = models.CharField(
        max_length=100, verbose_name='Razón social')
    direccion = models.CharField(
        max_length=200, null=True, blank=True, verbose_name='Dirección')
    representante = models.CharField(
        max_length=150, verbose_name='Representante legal')
    celular = models.CharField(max_length=20, verbose_name='Celular')
    email = models.EmailField(max_length=70, verbose_name='Email')
    # datos de contacto de facturacion
    contacto_nombre = models.CharField(
        max_length=150, null=True, blank=True, verbose_name='Nombre completo')
    contacto_celular = models.CharField(
        max_length=20, null=True, blank=True, verbose_name='Celular')
    contacto_email = models.EmailField(
        max_length=70, null=True, blank=True, verbose_name='Email')


    def __str__(self):
        return self.ruc + ' ' + self.razon_social

    class Meta:
        db_table = 'proveedor'
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveeedores'


class Compra(models.Model):
    id = models.BigAutoField(primary_key=True)
    fecha = models.DateField(verbose_name='Fecha', default=timezone.now)
    total = models.DecimalField(
        max_digits=9, decimal_places=2, verbose_name='Total', editable=False, default=0.00)
    proveedor = models.ForeignKey(
        Proveedor, on_delete=models.RESTRICT, verbose_name='Proveedor')
    serie = models.CharField(max_length=5, verbose_name='Serie')
    numero = models.CharField(max_length=10, verbose_name='Número')

    def __str__(self):
        return self.proveedor.razon_social + ' - Fecha: ' + str(self.fecha)
    

    # def save(self, *args, **kwargs):
    #     if self.id is None:
    #         pass
    #     else:
    #         # print(kwargs)
    #         if "actualizacion" in kwargs.keys():
    #             pass
    #         else:
    #             self.total = 0.00
    #     super().save()

    class Meta:
        db_table = 'compra'
        verbose_name = 'Compra'
        verbose_name_plural = 'Compras'


class DetalleCompra(models.Model):
    id = models.BigAutoField(primary_key=True)
    cantidad = models.PositiveSmallIntegerField(verbose_name='Cantidad')
    precio_unitario = models.DecimalField(
        max_digits=9, decimal_places=2, verbose_name='Precio unitario')
    compra = models.ForeignKey(
        Compra, on_delete=models.RESTRICT, verbose_name='Compra')
    presentacion = models.ForeignKey(
        Presentacion, on_delete=models.RESTRICT, verbose_name='Presentacion')

    def __str__(self):
        return self.presentacion.producto.titulo
    
    def save(self, *args, **kwargs):
        # aumentar el stock
        if self.id is None:
            print("actualizar stock")
            self.presentacion.stock = float(self.presentacion.stock) + float(self.cantidad)
            self.presentacion.save()
        else:
            # obtener lo que anteriormente se agrego
            # select * from detalle_compra where id = 5
            actual = DetalleCompra.objects.get(id=self.id)
            self.presentacion.stock = float(self.presentacion.stock) - float(actual.cantidad) + float(self.cantidad)
            self.presentacion.save() 

        super().save() # INSERT, UPDATE

        total = 0.00
        # consultando todos los detalles de la compra
        detalles = DetalleCompra.objects.filter(compra_id=self.compra.id)
        for item in detalles:
            total += float(item.cantidad) * float(item.precio_unitario)
        
        self.compra.total = total
        self.compra.save()

        # if self.id is None:
        #     total_actual = float(self.compra.total) 
        #     subtotal = float(self.cantidad) * float(self.precio_unitario) 
        #     total_actual += subtotal
        #     self.compra.total = total_actual
        #     self.compra.save() 
        # else:
        #     print("se detecta actualizacion" + str(self.id))
        #     total_actual = float(self.compra.total)
        #     subtotal = float(self.cantidad) * float(self.precio_unitario)
        #     total_actual += subtotal
        #     self.compra.total = total_actual
        #     self.compra.save(actualizacion=True)
        # super().save()

    class Meta:
        db_table = 'detalle_compra'
        verbose_name = 'Detelle de compras'
        verbose_name_plural = 'Detalles de compras'
