# Generated by Django 5.0 on 2024-01-11 02:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0002_categoria_descripcion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='categoria',
            name='descripcion',
        ),
    ]
