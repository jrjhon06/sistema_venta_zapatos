from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from productos.models import Presentacion, Producto
from django.urls import reverse
from online.forms import RegistrarseForm, LoginForm, AgregarItemForm, RegistrarPedidoForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from pedidos.models import Pedido, DetallePedido, Cliente
from datetime import date
from django.db import transaction

def portada(request):
    productos = Producto.objects.all()  # queryset
    return render(request, "online/portada.html", {"listado_productos": productos})


def agregar_item(request):
    if request.method == "POST":
        formAgregarItem = AgregarItemForm(request.POST)
        if (formAgregarItem.is_valid()):
            """
            [
                item1, item2, item3, item4......
            ]

            item = {
                "presentacion_id": ""
                "cantidad": ""
                "precio": ""
                "subtotal": ""
                "descripcion": ""
                "imagen": ""
            }
            """

            # recuperar la variable de session actual
            carrito_pedido = request.session.get("carrito_pedido", [])

            producto_id = formAgregarItem.cleaned_data["producto_id"]
            color_id = formAgregarItem.cleaned_data["color_id"]
            medida_id = formAgregarItem.cleaned_data["medida_id"]
            cantidad = formAgregarItem.cleaned_data["cantidad"]

            presentacion = Presentacion.objects.get(producto_id=producto_id,
                                                    color_id=color_id,
                                                    medida_id=medida_id)
            
            if cantidad > presentacion.stock:
                data = {"message": 'Stock no disponible'}
                return JsonResponse(data, status=409)

            subtotal = float(presentacion.producto.precio) * float(cantidad)

            descripcion = presentacion.producto.titulo + \
                "( " + presentacion.color.nombre + \
                " - " + presentacion.medida.nombre + " )"

            # PRODUCTO XYZ (VERDE - S)

            item = {
                "presentacion_id": presentacion.id,
                "cantidad": cantidad,
                "precio": float(presentacion.producto.precio),
                "subtotal": subtotal,
                "descripcion": descripcion,
                "imagen": presentacion.producto.imagenproducto_set.order_by('orden')[0].nombre.url
            }

            carrito_pedido.append(item)

            # actualizar variable de sesion
            request.session["carrito_pedido"] = carrito_pedido

            data = {
                "message": "Producto agregado correctamente",
            }

            return JsonResponse(data, status=200)

        else:
            """
            {
                "medida_id": [
                    "No existe presentacion",
                    "No existe presentacion",
                    "No existe presentacion",
                    "No existe presentacion",
                ]
            }
            """
            print(formAgregarItem.errors)
            message = "Error en los datos <br> <ul>"
            for erroresCampo in formAgregarItem.errors.values():
                for error in erroresCampo:
                    message += "<li>- " + error + "</li>"

            message += "</ul>"
            data = {
                "message": message,
            }

            return JsonResponse(data, status=422)
    pass


def quitar_item(request):
    if request.method == 'POST':
        indice = int(request.POST.get("indice"))
        try:
            carrito = request.session.get("carrito_pedido", [])
            del carrito[indice]
            request.session["carrito_pedido"] = carrito

            data = {"message": 'Producto removido correctamente'}

            return JsonResponse(data)
        except:
            data = {"message": 'Error al intentar quitar producto del carrito'}

            return JsonResponse(data, status=500)
    else:
        data = {"message": 'Metodo de la petición no permitido'}

        return JsonResponse(data, status=500)


def detalle_producto(request, slug_producto):
    try:
        producto = Producto.objects.get(slug=slug_producto)
        # PRODUCTO -> Presentacion(producto_id, color_id) -> COLORES
        # PRODUCTO -> Presentacion(producto_id, medida_id) -> MEDIDAS
        colores = producto.colores.distinct()
        medidas = producto.medidas.distinct()

        return render(request, "online/detalle-producto.html", {
            "producto": producto,
            "colores": colores,
            "medidas": medidas
        })

    except ObjectDoesNotExist as error:
        return render(request, "online/404.html", {
            "message": "El producto que estas buscando no existe"
        })


@login_required(login_url="/iniciar-sesion")
def mi_cuenta(request):
    return render(request, "online/mi-cuenta.html")


def cerrar_session(request):
    logout(request)
    ruta_portada = reverse("portada")
    return HttpResponseRedirect(ruta_portada)


def ingresar(request):
    if request.method == "POST":
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            email = login_form.cleaned_data["email"]
            password = login_form.cleaned_data["password"]

            usuario_logeado = authenticate(username=email, password=password)

            login(request, usuario_logeado)

            data = {"message": "Usuario ha iniciado sesión correctamente"}

            return JsonResponse(data, status=200)

        else:
            data = {
                "message": "Error en los datos",
                "errors": login_form.errors
            }

            return JsonResponse(data, status=422)
    else:
        ruta_formulario_loginm = reverse('iniciar_sesion')

        return HttpResponseRedirect(ruta_formulario_loginm)


def iniciar_sesion(request):
    return render(request, "online/iniciar-sesion.html")


def registrarse(request):
    return render(request, "online/registrarse.html")


def carrito(request):
    carrito = request.session.get("carrito_pedido", [])
    return render(request, "online/carrito.html", {"carrito": carrito})


def registrar_cliente(request):
    if request.method == 'POST':
        # request.POST -> toda la informacion
        formulario_registrarse = RegistrarseForm(request.POST)

        if formulario_registrarse.is_valid():
            nombres = formulario_registrarse.cleaned_data["nombres"]
            apellidos = formulario_registrarse.cleaned_data["apellidos"]
            email = formulario_registrarse.cleaned_data["email"]
            password = formulario_registrarse.cleaned_data["password"]

            # crear el usuario: auth_user
            usuario = User.objects.create_user(
                username=email,
                password=password,
                email=email,
                first_name=nombres,
                last_name=apellidos
            )
            # crear el cliente: cliente, lo relacionamos con el usuario
            cliente = Cliente()
            cliente.nombres = nombres
            cliente.apellidos = apellidos
            cliente.email = email
            cliente.usuario_id = usuario.id
            cliente.save()

            data = {
                "message": "Cliente registrado correctamente"
            }

            return JsonResponse(data, status=201)
        else:
            errores = formulario_registrarse.errors

            info = {
                "message": "Datos nos son validos, revisar por favor",
                "errors": errores
            }

            return JsonResponse(info, status=422)  # entidad improcesable

    else:
        ruta_formulario_registro = reverse('registrarse')

        return HttpResponseRedirect(ruta_formulario_registro)


def modificar_cantidad(request):
    if request.method == 'POST':
        try:
            cantidad = int(request.POST.get("cantidad"))
            indice = int(request.POST.get("indice"))
            carrito = request.session.get("carrito_pedido", [])
            item = carrito[indice]
            presentacion_id = item["presentacion_id"]

            presentacion = Presentacion.objects.get(id=presentacion_id)

            if cantidad > presentacion.stock:
                data = {"message": 'Stock no disponible'}
                return JsonResponse(data, status=409)

            subtotal = float(presentacion.producto.precio) * float(cantidad)

            descripcion = presentacion.producto.titulo + \
                "( " + presentacion.color.nombre + \
                " - " + presentacion.medida.nombre + " )"

            carrito[indice] = {
                "presentacion_id": presentacion.id,
                "cantidad": cantidad,
                "precio": float(presentacion.producto.precio),
                "subtotal": subtotal,
                "descripcion": descripcion,
                "imagen": presentacion.producto.imagenproducto_set.order_by('orden')[0].nombre.url
            }

            request.session["carrito_pedido"] = carrito
            data = {"message": 'Cantidad actualizada correctameten'}
            return JsonResponse(data, status=200)

        except Exception as error:
            data = {"message": 'Error al intentar actualizar la cantidad', "error": str(error)}
            return JsonResponse(data, status=500)

    else:
        data = {"message": 'Metodo de la petición no permitido'}
        return JsonResponse(data, status=405)




@login_required(login_url="/iniciar-sesion")
def confirmar_pedido(request):
    try:
        usuario = request.user
        cliente = Cliente.objects.get(usuario_id=usuario.id)
        data_inicial = {
            'nombres': cliente.nombres,
            'apellidos': cliente.apellidos,
            'dni': cliente.dni,
            'email': cliente.email,
            'celular': cliente.celular,
            'direccion': cliente.direccion,
        }
        formulario_datos = RegistrarPedidoForm(initial=data_inicial)
        return render(request, "online/confirmar_pedido.html", {'formulario_datos': formulario_datos})
    except ObjectDoesNotExist as error:
        return render(request, "online/mensaje.html", {
            "mensaje": "Usuario autenticado es administrativo, ingrese con un usuario de cliente para "
                       "registrar pedido"})
    
# @transaction.atomic
@login_required(login_url="/iniciar-sesion")
def guardar_pedido(request):
    if request.method == "POST":
        formulario = RegistrarPedidoForm(request.POST)
        if formulario.is_valid():
            try:
                with transaction.atomic():
                    # actualizar los datos del cliente
                    usuario_logeado = request.user
                    cliente = Cliente.objects.get()
                    cliente.nombres = request.POST.get("nombres")
                    cliente.apellidos = request.POST.get("apellidos")
                    cliente.email = request.POST.get("email")
                    cliente.dni = request.POST.get("dni")
                    cliente.direccion = request.POST.get("direccion")
                    cliente.celular = request.POST.get("celular")
                    cliente.save()

                    print("se actualizó cliente")

                    # actualizar los datos del usuario
                    usuario_logeado.first_name = request.POST.get("nombres")
                    usuario_logeado.last_name = request.POST.get("apellidos")
                    usuario_logeado.username = request.POST.get("email")
                    usuario_logeado.email = request.POST.get("email")
                    usuario_logeado.save()
                    print("se actualizó Usuario")

                    # registrar el pedido
                    carrito = request.session.get("carrito_pedido", [])

                    total = 0.00
                    for item in carrito:
                        total = total + item['subtotal']
                

                    pedido = Pedido()
                    pedido.fecha = date.today()
                    pedido.direccion = request.POST.get("direccion")
                    pedido.cliente_id = cliente.id
                    pedido.observacion = request.POST.get("observacion")
                    pedido.total = total
                    pedido.save()

                    print("se registro pedido")

                    # registrar el detalle del pedido y descontar el stock
                    

                    for item in carrito:
                        detalle_pedido = DetallePedido()
                        detalle_pedido.cantidad = int(item["cantidad"])
                        detalle_pedido.pedido_id = pedido.id
                        detalle_pedido.presentacion_id = item["presentacion_id"]
                        detalle_pedido.precio_unitario = item["precio"]
                        detalle_pedido.save()

                        # descontar el stock
                        presentacion = Presentacion.objects.get(id=item["presentacion_id"])
                        presentacion.stock = presentacion.stock - int(item["cantidad"])
                        presentacion.save()

                request.session["carrito_pedido"] = []

                url = reverse('mi_cuenta')
                return HttpResponseRedirect(url)
            except Exception as error:
                print(error)
                url = reverse('confirmar_pedido')
                return HttpResponseRedirect(url)
        else:
            print("errores de formulari")
            for campo_con_error in formulario.errors:
                formulario[campo_con_error].field.widget.attrs["class"]="form-control is-invalid"
            return render(request, "online/confirmar_pedido.html", {'formulario_datos': formulario})
    else:
        url = reverse('confirmar_pedido')
        return HttpResponseRedirect(url)