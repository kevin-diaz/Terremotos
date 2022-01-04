from django.db import models

# Tabla terremoto.
class Terremoto(models.Model):
    id = models.AutoField(primary_key=True)
    magnitud = models.DecimalField(max_digits=3,decimal_places=2,null=True)
    lugar = models.CharField(max_length=100,null=True)
    tiempo = models.DateField(auto_now=False,auto_now_add=False,null=True)
    tsunami = models.IntegerField(default=0,null=True)
    importancia = models.IntegerField(null=True)
    fecha_actualizacion = models.DateField(auto_now=False,auto_now_add=False,null=True)
    alerta = models.CharField(max_length=100,null=True)
    dispersion_profundidad = models.DecimalField(max_digits=6,decimal_places=2,null=True)
    tipo_movimiento = models.CharField(max_length=100,null=True)

    class Meta:
        verbose_name = "Terremoto"
        verbose_name_plural = "Terremotos"

    def __str__(self):
        return str(self.id)
