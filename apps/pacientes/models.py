from django.db import models
from django.conf import settings
 
# Create your models here.
class Pacientes(models.Model):
    nombre = models.CharField(max_length = 50)
    apellido = models.CharField(max_length = 50)
    historial = models.CharField(max_length = 500, null = True)

    def __str__(self):
        return "{} {}".format(self.nombre, self.apellido)

class Turnos(models.Model):

    OPT_ASISTENCIA = (
        ('P', 'Pendiente'),
        ('A', 'Asistió'),
        ('F', 'Faltó')
    )

    id_medico = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        limit_choices_to={'groups__name': 'Medico'}, 
        on_delete = models.CASCADE,
    )

    id_paciente = models.ForeignKey(Pacientes, on_delete = models.CASCADE)
    fecha = models.DateField()
    asistencia = models.CharField(max_length = 1, choices = OPT_ASISTENCIA)
    observacion = models.CharField(max_length = 250, null = True)

    def __str__(self):
        return "{}".format(self.id)