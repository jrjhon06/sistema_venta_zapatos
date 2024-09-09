from django.core.exceptions import ValidationError

def validar_ruc(value):
    if value is not None and value != '':
        if len(value) != 11:
            raise ValidationError("El RUC debe tener 11 caracteres")