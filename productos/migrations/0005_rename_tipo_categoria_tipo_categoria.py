# Generated by Django 5.0 on 2024-01-11 02:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0004_categoria_tipo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='categoria',
            old_name='tipo',
            new_name='tipo_categoria',
        ),
    ]