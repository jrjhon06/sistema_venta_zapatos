from django.contrib import admin
from productos.models import Categoria, Marca, Producto, Presentacion, ImagenProducto


admin.site.register(Categoria)

admin.site.register(Marca)


class PresentacionInline(admin.TabularInline):
    model = Presentacion



class ImagenProductoInline(admin.TabularInline):
    model = ImagenProducto



class ProductoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'activo', 'precio', 'marca', 'categoria', 'slug']
    search_fields = ['titulo', 'marca__nombre', 'categoria__nombre']
    list_filter = ['activo', 'marca', 'categoria']
    inlines = [PresentacionInline, ImagenProductoInline]
    actions = ["activar_productos", "desactivar_productos"]

    @admin.action(description="Activar productos seleccionados")
    def activar_productos(self, request, queryset):
        # print(request.method)
        usuario_actual = request.user
        print(usuario_actual)
        for producto in queryset:
            producto.activo = True
            producto.save()

    @admin.action(description="Desactivar productos seleccionados")
    def desactivar_productos(self, request, queryset):
        for producto in queryset:
            producto.activo = False
            producto.save()


admin.site.register(Producto, ProductoAdmin)


admin.site.register(Presentacion)


admin.site.register(ImagenProducto)
