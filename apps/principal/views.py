from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from .models import OPT_ROLES
from apps.pacientes.models import Pacientes
from apps.ventas.models import PedidosCab, Productos

def inicio(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    
    if request.user.groups.exists():
        grupo = request.user.groups.get()
        #print(grupo.name)
        if grupo.name == OPT_ROLES[0][1]:
            # Medico
            return HttpResponseRedirect(reverse("listado_turnos"))
        elif grupo.name == OPT_ROLES[1][1]:  
            # SECRETARIA
            return HttpResponseRedirect(reverse("listado_turnos"))
        elif grupo.name == OPT_ROLES[2][1]:  
            # Gerencia
            return HttpResponseRedirect(reverse("gerencia"))
        elif grupo.name == OPT_ROLES[3][1]:  
            # Venta
            return HttpResponseRedirect(reverse("listado_pedidos"))
        elif grupo.name == OPT_ROLES[4][1]:  
            # Taller
            return HttpResponseRedirect(reverse("listado_pedidos"))
    
    return HttpResponseRedirect(reverse("listado_turnos"))

def login_f(request):
    
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username = username, password = password)

        if user:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "users/login.html", {
                "mensaje" : "Los datos ingresados no son correctos"
            })
    else:
        if not request.user.is_authenticated:
            return render(request, "users/login.html")
        else:
            return HttpResponseRedirect(reverse("index"))

    return render(request, "users/login.html")

def logout_f(request):
    logout(request)
    return render(request, "users/login.html", {
        "mensaje" : "Sesión cerrada con éxito"
    })

def indexGerencia(request):
    return render(request, "gerencia/index.html")

def getReporte(request, tipo, fd, fh):
    
    if tipo == 'apac':
        pacientes = Pacientes.objects.raw("SELECT a.id, a.fecha, a.asistencia, a.id_medico_id, b.id as idPaciente, b.nombre, b.apellido from pacientes_turnos a LEFT JOIN pacientes_pacientes b on a.id_paciente_id = b.id where asistencia ='A' and (fecha>='{}' and fecha<='{}')".format(fd, fh))
        
        return render(request, "gerencia/rp_pacientes.html", {
            "lista" : pacientes,
            "titulo" : "Asistencias por pacientes ({} al {})".format(fd, fh)
        })
    elif tipo == 'ipac':  
        pacientes = Pacientes.objects.raw("SELECT a.id, a.fecha, a.asistencia, a.id_medico_id, b.id as idPaciente, b.nombre, b.apellido from pacientes_turnos a LEFT JOIN pacientes_pacientes b on a.id_paciente_id = b.id where asistencia <> 'A' and (fecha>='{}' and fecha<='{}')".format(fd, fh))
        
        return render(request, "gerencia/rp_pacientes.html", {
            "lista" : pacientes,
            "titulo" : "Inasistencias por pacientes ({} al {})".format(fd, fh)
        })
    elif tipo == 'ppac':  
        pedidos = PedidosCab.objects.raw("SELECT 1 as id, count(a.id) as cantidad,SUM(a.total) as total,b.id as idPaciente,b.nombre,b.apellido FROM ventas_pedidoscab a LEFT JOIN pacientes_pacientes b on a.paciente_id = b.id WHERE (a.fecha>='{}' and a.fecha<='{}') GROUP BY b.id,b.nombre,b.apellido".format(fd, fh))
        return render(request, "gerencia/rp_pacientes_pedidos.html", {
            "lista" : pedidos,
            "titulo" : "Pedidos por pacientes ({} al {})".format(fd, fh)
        })
    elif tipo == 'pvend':  
        ventas = Productos.objects.raw("SELECT 1 as id, count(a.id) as cantidad,a.producto_id,c.descripcion,sum(a.cantidad) as vendidos,(a.cantidad*a.unitario) as total FROM ventas_pedidosdet a LEFT JOIN ventas_pedidoscab b on a.pedido_id = b.id LEFT JOIN ventas_productos c on a.producto_id = c.id WHERE (b.fecha>='{}' and b.fecha<='{}') GROUP by a.producto_id,c.descripcion ORDER BY vendidos desc".format(fd, fh))
        return render(request, "gerencia/rp_prodvendidos.html", {
            "lista" : ventas,
            "titulo" : "Productos más vendidos ({} al {})".format(fd, fh)
        })
    elif tipo == 'vvend':  
        ventas = Productos.objects.raw("SELECT 1 as id, sum(a.total) as total, a.vendedor_id,b.first_name FROM ventas_pedidoscab a LEFT JOIN auth_user b on a.vendedor_id = b.id WHERE (fecha>='{}' and fecha<='{}') GROUP BY a.vendedor_id,b.first_name".format(fd, fh))
        return render(request, "gerencia/rp_ventasvendedor.html", {
            "lista" : ventas,
            "titulo" : "Productos más vendidos ({} al {})".format(fd, fh)
        })
    