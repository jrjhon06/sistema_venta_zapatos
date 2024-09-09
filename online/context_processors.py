def total_carrito(request):
    total = 0.00
    carrito = request.session.get("carrito_pedido", [])
    for item in carrito:
        total += item["subtotal"]

    return {"total_carrito": total}


def cantidad_items(request):
    carrito = request.session.get("carrito_pedido", [])
    cantidad_items = len(carrito)

    return {"cantidad_items": cantidad_items}


def listado_carrito(request):
    carrito = request.session.get("carrito_pedido", [])

    return {"listado_carrito": carrito}