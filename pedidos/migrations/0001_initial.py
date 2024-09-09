# Generated by Django 5.0 on 2024-03-07 01:51

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('productos', '0014_producto_colores_producto_medidas'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.CharField(max_length=100, verbose_name='Número')),
                ('fecha', models.DateField(verbose_name='Fecha')),
                ('total', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Total')),
                ('direccion', models.CharField(max_length=200, verbose_name='Dirección')),
                ('observacion', models.CharField(max_length=500, verbose_name='Dirección')),
            ],
            options={
                'verbose_name': 'Pedido',
                'verbose_name_plural': 'Pedidos',
                'db_table': 'pedido',
            },
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('nombres', models.CharField(max_length=50, verbose_name='Nombres')),
                ('apellidos', models.CharField(max_length=50, verbose_name='Apellidos')),
                ('email', models.EmailField(max_length=70, verbose_name='Email')),
                ('dni', models.CharField(max_length=8, null=True, verbose_name='DNI')),
                ('celular', models.CharField(max_length=20, null=True, verbose_name='Celular')),
                ('telefono', models.CharField(max_length=20, null=True, verbose_name='Teléfono')),
                ('direccion', models.CharField(max_length=200, null=True, verbose_name='Dirección')),
                ('fecha_nacimiento', models.DateField(max_length=200, null=True, verbose_name='Fecha de nacimiento')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Clientes',
                'db_table': 'cliente',
            },
        ),
        migrations.CreateModel(
            name='DetallePedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveSmallIntegerField(verbose_name='Cantidad')),
                ('precio_unitario', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Precio unitario')),
                ('presentacion', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='productos.presentacion', verbose_name='Presentación')),
                ('pedido', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='pedidos.pedido', verbose_name='Pedido')),
            ],
            options={
                'verbose_name': 'Detalle de pedido',
                'verbose_name_plural': 'Detalles de pedidos',
                'db_table': 'detalle_pedido',
            },
        ),
    ]