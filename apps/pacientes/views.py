from django.shortcuts import render, redirect
#from django.contrib.auth.models import User, Group
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Turnos, Pacientes
from .forms import TurnoForm

# Create your views here.
def listarTurno(request):
    
    data = [] 
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
                'paciente': paciente.nombre,
                'idmedico': turno.id_medico_id,
                'medico': medico.first_name + medico.last_name,
                'fecha': turno.fecha,
                'asistencia': asis
            }
        )

    return render(request, "pacientes/listado_turnos.html", {
        "data" : data
    })

def altaTurno(request):
    print(request.user.is_authenticated)
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    if request.method == 'GET':
        form = TurnoForm()        
    else:
        form = TurnoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listado_turnos')
            
    contexto = {'form': form}
    return render(request, 'pacientes/alta_turno.html', contexto)

def editarTurno(request, id):
    turno = Turnos.objects.get(id = id)
    if request.method == 'GET':
        form = TurnoForm(instance = turno)
    else:
        form = TurnoForm(request.POST, instance = turno)
        if form.is_valid():
            form.save()
            return redirect('listado_turnos')

    contexto = {'form': form, 'editando': True}

    return render(request, 'pacientes/alta_turno.html', contexto)

def eliminarTurno(request, id):
    turno = Turnos.objects.get(id = id)
    turno.delete()
    return redirect('listado_turnos')