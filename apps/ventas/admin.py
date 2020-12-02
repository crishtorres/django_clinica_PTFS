from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Productos)
admin.site.register(models.PedidosCab)
admin.site.register(models.PedidosDet)