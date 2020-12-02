from django.shortcuts import render, redirect
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse, HttpResponseRedirect
import json as simplejson
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import User
from .models import Turnos, Pacientes
from .forms import TurnoForm, HistorialForm, PacientesForm


class TurnoList(ListView):
    model = Turnos
    template_name = 'pacientes/listado_turnos.html'

    def get_queryset(self):
        #return self.model.objects.all()
        f_fecha = self.request.GET.get('fecha')
        print(f_fecha)
        data = [] 

        rol = self.request.user.groups.get()

        if rol.name == 'Medico':
            self.template_name = 'medico/listado_turnos.html'

            if f_fecha:
                turn = Turnos.objects.filter(id_medico_id = self.request.user.id).filter(fecha = f_fecha)
            else:
                turn = Turnos.objects.filter(id_medico_id = self.request.user.id)
        else:
            turn = Turnos.objects.all()
        
        for turno in turn:
            paciente = Pacientes.objects.get(id = turno.id_paciente_id)
            medico = User.objects.get(id = turno.id_medico_id)

            if turno.asistencia == 'P':
                asis = 'Pendiente'
            elif turno.asistencia == 'A':
                asis = 'Asistió'
            else:
                asis = 'Faltó'

            data.append(
                {
                    'id': turno.id,
                    'idpaciente': turno.id_paciente_id,
                    'paciente': paciente.nombre + ' ' + paciente.apellido,
                    'idmedico': turno.id_medico_id,
                    'medico': medico.first_name + ' ' + medico.last_name,
                    'fecha': turno.fecha,
                    'asistencia': asis,
                    'historial': paciente.historial
                }
            )

        return data

class TurnoCreate(CreateView):

    model = Turnos
    form_class = TurnoForm
    template_name = 'pacientes/alta_turno.html'
    success_url = reverse_lazy('listado_turnos')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        resp = super(TurnoCreate, self).dispatch(*args, **kwargs)
        grupo = self.request.user.groups.get()

        if not self.request.user.is_authenticated or (grupo.name != 'Secretaria' and grupo.name != 'Gerencia'):
            return HttpResponseRedirect(reverse("login"))
        else:
            return resp

class TurnoEdit(UpdateView):
    model = Turnos
    form_class = TurnoForm
    template_name = 'pacientes/alta_turno.html'
    success_url = reverse_lazy('listado_turnos')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        resp = super(TurnoEdit, self).dispatch(*args, **kwargs)
        grupo = self.request.user.groups.get()

        if not self.request.user.is_authenticated or (grupo.name != 'Secretaria' and grupo.name != 'Gerencia'):
            return HttpResponseRedirect(reverse("login"))
        else:
            return resp

class TurnoDelete(DeleteView):
    model = Turnos
    template_name = 'pacientes/verificacion.html'
    success_url = reverse_lazy('listado_turnos')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        
        resp = super(TurnoDelete, self).dispatch(*args, **kwargs)
        grupo = self.request.user.groups.get()

        if not self.request.user.is_authenticated or (grupo.name != 'Secretaria' and grupo.name != 'Gerencia'):
            return HttpResponseRedirect(reverse("login"))
        elif self.request.is_ajax():
            response_data = {"result": "ok"}
            return HttpResponse(simplejson.dumps(response_data),
                content_type="application/json")
        else:
            return resp

class HisMedicoEdit(UpdateView):
    model = Pacientes
    form_class = HistorialForm
    template_name = 'medico/historial.html'
    success_url = reverse_lazy('listado_turnos')


class PacientesList(ListView):
    model = Pacientes
    template_name = 'pacientes/listado_pacientes.html'

class PacientesCreate(CreateView):

    model = Pacientes
    form_class = PacientesForm
    template_name = 'pacientes/alta_paciente.html'
    success_url = reverse_lazy('listado_pacientes')

class PacientesEdit(UpdateView):
    model = Pacientes
    form_class = PacientesForm
    template_name = 'pacientes/alta_paciente.html'
    success_url = reverse_lazy('listado_pacientes')

class PacientesDelete(DeleteView):
    model = Pacientes
    template_name = 'pacientes/verificacion.html'
    success_url = reverse_lazy('listado_pacientes')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        
        resp = super(PacientesDelete, self).dispatch(*args, **kwargs)
        grupo = self.request.user.groups.get()

        if not self.request.user.is_authenticated or (grupo.name != 'Secretaria' and grupo.name != 'Gerencia'):
            return HttpResponseRedirect(reverse("login"))
        elif self.request.is_ajax():
            response_data = {"result": "ok"}
            return HttpResponse(simplejson.dumps(response_data),
                content_type="application/json")
        else:
            return resp


