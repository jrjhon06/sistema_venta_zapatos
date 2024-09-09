# Generated by Django 5.0 on 2024-01-23 01:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('productos', '0011_imagenproducto'),
    ]

    operations = [
        migrations.CreateModel(
            name='Compra',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('fecha', models.DateField(verbose_name='Fecha')),
                ('total', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Total')),
                ('serie', models.CharField(max_length=5, verbose_name='Serie')),
                ('numero', models.CharField(max_length=10, verbose_name='Número')),
            ],
            options={
                'verbose_name': 'Compra',
                'verbose_name_plural': 'Compras',
                'db_table': 'compra',
            },
        ),
        migrations.CreateModel(
            name='Proveedor',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('ruc', models.CharField(max_length=11, verbose_name='RUC')),
                ('razon_social', models.CharField(max_length=100, verbose_name='Razón social')),
                ('direccion', models.CharField(blank=True, max_length=200, null=True)),
                ('representante', models.CharField(max_length=150)),
                ('celular', models.CharField(max_length=20)),
                ('email', models.CharField(max_length=70)),
            ],
            options={
                'verbose_name': 'Proveedor',
                'verbose_name_plural': 'Proveeedores',
                'db_table': 'proveedor',
            },
        ),
        migrations.CreateModel(
            name='DetalleCompra',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('cantidad', models.PositiveSmallIntegerField(verbose_name='Cantidad')),
                ('precio_unitario', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Precio unitario')),
                ('compra', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='compras.compra', verbose_name='Compra')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='productos.producto', verbose_name='Producto')),
            ],
            options={
                'verbose_name': 'Detelle de compras',
                'verbose_name_plural': 'Detalles de compras',
                'db_table': 'detalle_compra',
            },
        ),
        migrations.AddField(
            model_name='compra',
            name='proveedor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='compras.proveedor', verbose_name='Proveedor'),
        ),
    ]
