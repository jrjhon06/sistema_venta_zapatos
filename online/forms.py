from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from productos.models import Presentacion
from django.core.exceptions import ObjectDoesNotExist


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=50, required=True)
    password = forms.CharField(max_length=50, required=True)

    def clean(self):
        cleaned_data = super().clean()

        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        # validar que exista usuario con el email
        if email is not None:
            cantidad_usuarios = User.objects.filter(username=email).count()

            if cantidad_usuarios == 0:
                self.add_error("email", "Correo no existe")

            if password is not None:

                usuario = authenticate(username=email, password=password)

                if usuario is None:
                    self.add_error("password", "Contraseña incorrecta")


class RegistrarseForm(forms.Form):
    nombres = forms.CharField(max_length=50, required=True)
    apellidos = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(max_length=70, required=True)
    password = forms.CharField(max_length=70, required=True)
    confirmar_password = forms.CharField(max_length=70, required=True)

    def clean(self):
        cleaned_data = super().clean()

        # que el campo password y confimar_password sean iguales
        password = cleaned_data.get("password")
        confirmar_passwrd = cleaned_data.get("confirmar_password")

        if password != confirmar_passwrd:
            self.add_error("password", "Las contraseñas no coinciden")
            self.add_error("confirmar_password",
                           "Las contraseñas no coinciden")

        # no exista otro usuario con el mismo email
        email = cleaned_data.get("email")

        cantidad_usuarios = User.objects.filter(username=email).count()

        if cantidad_usuarios > 0:
            self.add_error("email", "Este correo electrónico ya está en uso")


class AgregarItemForm(forms.Form):
    producto_id = forms.IntegerField(required=True)
    color_id = forms.IntegerField(required=True)
    medida_id = forms.IntegerField(required=True)
    cantidad = forms.IntegerField(required=True)

    def clean(self):
        cleaned_data = super().clean()

        try:
            producto_id = cleaned_data.get("producto_id")
            color_id = cleaned_data.get("color_id")
            medida_id = cleaned_data.get("medida_id")
            cantidad = cleaned_data.get("cantidad")

            # 1. Presentacion exista:
            presentacion = Presentacion.objects.get(
                producto_id=producto_id,
                color_id=color_id,
                medida_id=medida_id
            )

            # 2. Validar el stock
            if presentacion.stock < cantidad:
                self.add_error("medida_id", "Stock no disponible")

        except ObjectDoesNotExist as error:
            self.add_error("medida_id", "No existe presentación")


class RegistrarPedidoForm(forms.Form):
    nombres = forms.CharField(label="Nombres", max_length=100, required=True,
                              widget=forms.TextInput(attrs={'placeholder': 'Nombres'}))
    apellidos = forms.CharField(
        label="Apellidos", max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Apellidos'}))
    email = forms.EmailField(label="Correo electrónico",
                             max_length=100, required=True,
                             widget=forms.EmailInput(attrs={'placeholder': 'Correo electrónico'}))
    dni = forms.CharField(label="DNI", max_length=100, required=True,
                          widget=forms.TextInput(attrs={'placeholder': 'Ingresar DNI'}))
    direccion = forms.CharField(label="Dirección", max_length=100, required=True,
                                widget=forms.TextInput(attrs={'placeholder': 'Ingresar dirección'}))
    celular = forms.CharField(label="Celular", max_length=100, required=True,
                              widget=forms.TextInput(attrs={'placeholder': 'Ingresar celular'}))
    observacion = forms.CharField(label="Observación", max_length=100, required=False,
                                  widget=forms.Textarea(attrs={'placeholder': 'Ingresar observación(opcional)'}))

    def clean(self):
        cleaned_data = super().clean()
        dni = cleaned_data.get("dni")
        if dni is not None and len(dni) != 8:
            self.add_error("dni", "DNI no es válido")
