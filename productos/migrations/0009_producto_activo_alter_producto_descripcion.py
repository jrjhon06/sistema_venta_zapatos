# Generated by Django 5.0 on 2024-01-18 02:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0008_producto'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='activo',
            field=models.BooleanField(default=True, verbose_name='¿Activo?'),
        ),
        migrations.AlterField(
            model_name='producto',
            name='descripcion',
            field=models.TextField(blank=True, null=True, verbose_name='Descripción'),
        ),
    ]
