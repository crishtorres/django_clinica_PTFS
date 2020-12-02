from django.shortcuts import render, redirect
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import json as simplejson
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from .models import PedidosCab, PedidosDet, Productos
from apps.pacientes.models import Pacientes
from .forms import PedidosForm, PedidosDetForm, StatusForm, ProductosForm

class PedidosList(ListView):
    model = PedidosCab
    template_name = 'ventas/listado_ventas.html'

    def get_queryset(self):
        data = []

        if not self.request.user.is_authenticated:
            return HttpResponseRedirect("login")

        rol = self.request.user.groups.get()

        if rol.name == 'Ventas' or rol.name == 'Gerencia':
            #Venta
            ped = PedidosCab.objects.all()
        else:
            #Taller
            ped = PedidosCab.objects.filter(estado = 'T')
            self.template_name = 'ventas/listado_ventas_taller.html'

        for pedido in ped:
            # det = PedidosDet.objects.get(pedido_id = pedido.id)
            #medico = User.objects.get(id = turno.id_medico_id)    
            if pedido.estado == 'F':
                estado = 'Finalizado'
            elif pedido.estado == 'T':
                estado = 'Taller'
            elif pedido.estado == 'O':
                estado = 'Pedido'
            else:
                estado = 'Pendiente'

            data.append(
                {
                    'id': pedido.id,
                    'estado': estado,
                    'vendedor': pedido.vendedor,
                    'total': pedido.total,
                    'fecha': pedido.fecha,
                    'paciente': pedido.paciente
                }
            )
            
        return data

def getDetallePedido(request, id):

    rol = request.user.groups.get()
    
    det = PedidosDet.objects.filter(pedido_id = id)
    data = []

    for d in det:
        if d.lado == 'I':
            lado = 'Izquierdo'
        elif d.lado == 'D':
            lado = 'Derecho'
        else:
            lado = '-'

        if d.armazon == 'S':
            armazon = 'SI'
        else:
            armazon = 'NO'

        if d.cercania == 'L':
            cercania = 'Lejos'
        elif d.cercania == 'C':
            cercania = 'Cerca'
        else:
            cercania = '-'

        data.append(
            {
                'id': d.id,
                'producto': d.producto,
                'cantidad': d.cantidad,
                'unitario': d.unitario,
                'armazon': armazon,
                'lado': lado,
                'cercania': cercania,
                'total': float(d.cantidad) * float(d.unitario) 
            }
        )
    context = {
        'productos': data,
        'rol': rol.name
    }
    return render(request, "ventas/detalle_pedido.html", context)

def altaPedido(request):

    if not request.user.is_authenticated:
        return HttpResponseRedirect("login")

    productos = Productos.objects.all()
    
    if request.method == 'POST':
        pedido_form = PedidosForm(request.POST)
        pdet_form = PedidosDetForm(request.POST)

        if pedido_form.is_valid():

            print(request.POST)

            estado = "P"
            fecha = request.POST['fecha']
            pago = request.POST['pago']
            paciente = Pacientes.objects.get(id = request.POST['paciente'])

            total = 0
            for u, c in zip(request.POST.getlist('unitarios'),request.POST.getlist('cantidades')):
                if c:
                    total = total + (float(c)*float(u))

            cab = PedidosCab(estado = estado, fecha = fecha, vendedor = request.user, pago = pago, total = total, paciente = paciente)
            cab.save()
            iscab = PedidosCab.objects.latest('id')

            for prods, lados, arma, cantidades, cercanias, unitarios, clasif in zip(request.POST.getlist('productos'),request.POST.getlist('lados'),request.POST.getlist('armazones'),request.POST.getlist('cantidades'),request.POST.getlist('cercanias'),request.POST.getlist('unitarios'),request.POST.getlist('clasificaciones')):
                print(prods)
                if prods:                
                    det = PedidosDet()
                    det.cantidad = cantidades
                    det.unitario = unitarios
                    det.pedido_id = iscab.id
                    det.producto_id = prods
                    det.armazon = arma
                    det.cercania = cercanias
                    det.clasificacion = clasif
                    det.lado = lados
                    det.save()
                    
            return HttpResponseRedirect('listado_pedidos')        
        else:
            context = {
                'pedido_form': pedido_form,
                'pedidoDet_form': pdet_form,     
                'productos': productos,    
                'alta': True,
                'rolventas': True      
            }
    else:
        context = {
            'pedido_form': PedidosForm(),
            'pedidoDet_form': PedidosDetForm(),
            'productos': productos,
            'alta': True,
            'rolventas': True
        }

    return render(request, "ventas/alta_pedido.html", context)

def getDatosProducto(request, id):

    datos = list(Productos.objects.filter(id = id).values())
    
    return HttpResponse(simplejson.dumps(datos),
                content_type="application/json")

class StatusPedidoEdit(UpdateView):
    model = PedidosCab
    form_class = StatusForm
    template_name = 'ventas/estado.html'
    success_url = reverse_lazy('listado_pedidos')

    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        estados = []

        estados.append({'cod': 'P','desc': 'Pedido'})
        estados.append({'cod': 'T','desc': 'Taller'})

        context['estados'] = estados
        return context

def finalizarPedido(request, id):
    pedido = PedidosCab.objects.get(id = id)
    pedido.estado = 'F'
    pedido.save()
    return redirect('listado_pedidos')

class ProductosList(ListView):
    model = Productos
    template_name = 'productos/listado_productos.html'

class ProductosCreate(CreateView):

    model = Productos
    form_class = ProductosForm
    template_name = 'productos/alta_producto.html'
    success_url = reverse_lazy('listado_productos')

class ProductosEdit(UpdateView):
    model = Productos
    form_class = ProductosForm
    template_name = 'productos/alta_producto.html'
    success_url = reverse_lazy('listado_productos')

class ProductosDelete(DeleteView):
    model = Productos
    template_name = 'productos/verificacion.html'
    success_url = reverse_lazy('listado_productos')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        
        resp = super(ProductosDelete, self).dispatch(*args, **kwargs)
        grupo = self.request.user.groups.get()

        if not self.request.user.is_authenticated or (grupo.name != 'Secretaria' and grupo.name != 'Gerencia'):
            return HttpResponseRedirect(reverse("login"))
        elif self.request.is_ajax():
            response_data = {"result": "ok"}
            return HttpResponse(simplejson.dumps(response_data),
                content_type="application/json")
        else:
            return resp