from django.db import models

class Color(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(verbose_name="Nombre", max_length=50)

    def __str__(self):
        return self.nombre
    

    class Meta:
        db_table = 'color'
        verbose_name = 'Color'
        verbose_name_plural = 'Colores'



class Medida(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(verbose_name="Nombre", max_length=50)

    def __str__(self):
        return self.nombre
    

    class Meta:
        db_table = 'medida'
        verbose_name = 'Medida'
        verbose_name_plural = 'Medidas'