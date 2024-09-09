from django.contrib import admin
from compras.models import Proveedor, Compra, DetalleCompra


class ProveedorAdmin(admin.ModelAdmin):
    list_display = ['ruc', 'razon_social', 'email', 'representante', 'celular']
    # fieldsets
    fieldsets = (
        (
            'Datos básicos', {
                'fields': (
                    ('ruc', 'razon_social', 'direccion'),
                )
            }
        ),
        (
            'Datos de contacto de la empresa', {
                'fields': (
                    ('celular', 'representante'),
                    'email'
                )
            }
        ),
        (
            'Datos de contacto de facturación', {
                'fields': (
                    'contacto_nombre',
                    'contacto_celular',
                    'contacto_email'
                )
            }
        )
    )
    search_fields = ['ruc', 'razon_social']


admin.site.register(Proveedor, ProveedorAdmin)

class DetalleCompraInline(admin.TabularInline):
    model = DetalleCompra


class CompraAdmin(admin.ModelAdmin):
    list_display = ["fecha", "total", "proveedor", "serie", "numero"]
    search_fields = ["proveedor", "serie", "numero"]
    inlines = [DetalleCompraInline]
    autocomplete_fields = ['proveedor']
    # raw_id_fields = ['proveedor']


admin.site.register(Compra, CompraAdmin)
admin.site.register(DetalleCompra)
