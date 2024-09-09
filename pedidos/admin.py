from django.contrib import admin
from pedidos.models import Cliente, Pedido, DetallePedido

# Register your models here.
admin.site.register(Cliente)
admin.site.register(Pedido)
admin.site.register(DetallePedido)