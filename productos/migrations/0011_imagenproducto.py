# Generated by Django 5.0 on 2024-01-23 00:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0010_presentacion'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImagenProducto',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('nombre', models.ImageField(max_length=200, upload_to='productos', verbose_name='Nombre')),
                ('orden', models.PositiveSmallIntegerField(verbose_name='Orden')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='productos.producto', verbose_name='Producto')),
            ],
            options={
                'verbose_name': 'Imagen de producto',
                'verbose_name_plural': 'Imagenes de productos',
                'db_table': 'imagen_producto',
            },
        ),
    ]