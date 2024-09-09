# Generated by Django 5.0 on 2024-02-22 02:34

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0012_alter_categoria_tipo_categoria'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='slug',
            field=autoslug.fields.AutoSlugField(always_update=True, editable=False, null=True, populate_from='titulo', unique=['titulo']),
        ),
    ]