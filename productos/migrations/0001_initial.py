# Generated by Django 5.0 on 2024-01-11 01:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'categoria',
            },
        ),
    ]
