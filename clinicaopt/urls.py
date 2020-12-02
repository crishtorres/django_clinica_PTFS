"""clinicaopt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from apps.principal.views import inicio, login_f, logout_f, indexGerencia, getReporte
from apps.pacientes.views import listarTurno, altaTurno, editarTurno, eliminarTurno
from apps.pacientes.class_view import TurnoList, TurnoCreate, TurnoEdit, TurnoDelete, HisMedicoEdit, PacientesCreate, PacientesList, PacientesEdit, PacientesDelete
from apps.ventas.views import PedidosList, altaPedido, getDatosProducto, StatusPedidoEdit, finalizarPedido, getDetallePedido, ProductosCreate, ProductosDelete, ProductosEdit, ProductosList

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', inicio, name = 'index'),
    path('login', login_f, name = 'login'),
    path('logout', logout_f, name = 'logout'),
    path('accounts/login/', login_f, name = 'accounts/login/'),
    path('listado_turnos', TurnoList.as_view(), name = 'listado_turnos'),
    path('alta_turno', TurnoCreate.as_view(), name = 'alta_turno'),
    path('editar_turno/<int:pk>', TurnoEdit.as_view(), name = 'editar_turno'),
    path('eliminar_turno/<int:pk>', TurnoDelete.as_view(), name = 'eliminar_turno'),
    path('ver_historial/<int:pk>', HisMedicoEdit.as_view(), name = 'ver_historial'),
    path('listado_pedidos', PedidosList.as_view(), name = 'listado_pedidos'),
    path('alta_pedido', altaPedido, name = 'alta_pedido'),
    path('get_datos_producto/<int:id>', getDatosProducto, name = 'get_datos_producto'),
    path('modificar_estado/<int:pk>', StatusPedidoEdit.as_view(), name = 'modificar_estado'),
    path('finalizar_pedido/<int:id>', finalizarPedido, name = 'finalizar_pedido'),
    path('get_detalle_pedido/<int:id>', getDetallePedido, name = 'get_detalle_pedido'),
    path('gerencia', indexGerencia, name = 'gerencia'),
    path('get_reporte/<str:tipo>/<str:fd>/<str:fh>', getReporte, name = 'get_reporte'),
    path('listado_pacientes', PacientesList.as_view(), name = 'listado_pacientes'),
    path('alta_paciente', PacientesCreate.as_view(), name = 'alta_paciente'),
    path('editar_paciente/<int:pk>', PacientesEdit.as_view(), name = 'editar_paciente'),
    path('eliminar_paciente/<int:pk>', PacientesDelete.as_view(), name = 'eliminar_paciente'),
    path('listado_productos', ProductosList.as_view(), name = 'listado_productos'),
    path('alta_producto', ProductosCreate.as_view(), name = 'alta_producto'),
    path('editar_producto/<int:pk>', ProductosEdit.as_view(), name = 'editar_producto'),
    path('eliminar_producto/<int:pk>', ProductosDelete.as_view(), name = 'eliminar_producto')
]
