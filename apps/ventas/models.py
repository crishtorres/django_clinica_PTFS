from django.db import models
from django.conf import settings
from apps.pacientes.models import Pacientes

# Create your models here.
# tabla pedidos y tabla articulos

class Productos(models.Model):
    
    OPT_CLASIFICACION = (
        ('L', 'Lentes'),
        ('O', 'Otros')
    )
    codigo = models.CharField(max_length = 50)
    descripcion = models.CharField(max_length = 100)
    precio = models.FloatField()
    clasificacion = models.CharField(max_length = 1, choices = OPT_CLASIFICACION, null = True)
    
    def __str__(self):
        return "{} - {}".format(self.codigo, self.descripcion)

class PedidosCab(models.Model):

    OPT_ESTADOS = (
        ('P', 'Pendiente'),
        ('O', 'Pedido'),
        ('T', 'Taller'),
        ('F', 'Finalizado')
    )

    OPT_PAGOS = (
        ('C', 'Credito'),
        ('D', 'Debito'),
        ('V', 'Billetera virtual'),
        ('E', 'Efectivo')
    )
    
    estado = models.CharField(max_length = 1, choices = OPT_ESTADOS)
    fecha = models.DateField()
    vendedor = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        limit_choices_to={'groups__name': 'Venta'}, 
        on_delete = models.CASCADE,
    )
    paciente = models.ForeignKey(Pacientes, on_delete = models.CASCADE, null = True)
    pago = models.CharField(max_length = 1, choices = OPT_PAGOS)
    total = models.FloatField(default = 0)

class PedidosDet(models.Model):
    OPT_LADO = (
        ('I', 'Izquierda'),
        ('D', 'Derecha'),
        ('N', 'Ninguno')
    )

    OPT_CERCANIA = (
        ('L', 'Lejos'),
        ('C', 'Cerca'),
        ('N', 'Ninguno')
    )

    OPT_CLASIFICACION = (
        ('L', 'Lentes'),
        ('O', 'Otros')
    )

    pedido = models.ForeignKey(PedidosCab, on_delete = models.CASCADE)
    producto = models.ForeignKey(Productos, on_delete = models.CASCADE, null = True)
    cantidad = models.FloatField(null = True)
    unitario = models.FloatField(null = True)
    lado = models.CharField(max_length = 1, choices = OPT_LADO, null = True, default = 'N')
    cercania = models.CharField(max_length = 1, choices = OPT_CERCANIA, default = 'N')
    armazon = models.CharField(max_length = 1, null = True, choices = (('S', 'SI'), ('N', 'NO')), default = 'N')
    clasificacion = models.CharField(max_length = 1, choices = OPT_CLASIFICACION, null = True)