from django.urls import path
from online.views import agregar_item, detalle_producto, \
    cerrar_session, portada, iniciar_sesion, \
    registrarse, carrito, registrar_cliente, \
    ingresar, mi_cuenta, quitar_item, modificar_cantidad, \
    confirmar_pedido, guardar_pedido

urlpatterns = [
    path('', portada, name="portada"),
    path('iniciar-sesion', iniciar_sesion, name="iniciar_sesion"),
    path('ingresar', ingresar, name="ingresar"),
    path('registrarse', registrarse, name="registrarse"),
    path('registrar-cliente', registrar_cliente, name='registrar_cliente'),
    path('carrito', carrito, name="carrito"),
    path('mi-cuenta', mi_cuenta, name="mi_cuenta"),
    path('logout', cerrar_session, name="cerrar_sesion"),
    path('detalle-producto/<slug:slug_producto>',
         detalle_producto, name="detalle_producto"),
    path('carrito/agregar-item', agregar_item, name="carrito.agregar_item"),
    path('carrito/quitar-item', quitar_item, name="carrito.quitar_item"),
    path('carrito/modificar-cantidad', modificar_cantidad,
         name="carrito.modificar_cantidad"),
    path('confirmar-pedido', confirmar_pedido, name="confirmar_pedido"),
    path('guardar-pedido', guardar_pedido, name="guardar_pedido"),
]
