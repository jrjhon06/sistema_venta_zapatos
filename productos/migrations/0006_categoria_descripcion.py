# Generated by Django 5.0 on 2024-01-11 02:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0005_rename_tipo_categoria_tipo_categoria'),
    ]

    operations = [
        migrations.AddField(
            model_name='categoria',
            name='descripcion',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]