from django import forms
from .models import Turnos, Pacientes

class TurnoForm(forms.ModelForm):

    class Meta:
        model = Turnos
        fields = ('id','fecha','id_medico','id_paciente','asistencia','observacion')

        widgets = {
            'fecha': forms.DateInput(attrs={'class':'form-control', 'type': 'date'}),
            'asistencia': forms.Select(attrs={'class': 'form-control'}),
            'id_medico': forms.Select(attrs={'class': 'form-control'}),
            'id_paciente': forms.Select(attrs={'class': 'form-control'}),
            'observacion': forms.Textarea(attrs={'class': 'form-control', 'rows':'3'})
        }

        #widgets = {'fecha': forms.DateInput}
        # fecha = forms.DateField(widget = forms.DateInput(attrs = {'class':'form-control'}))
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_medico'].label = "Medico"
        self.fields['id_paciente'].label = "Paciente"

class HistorialForm(forms.ModelForm):

    class Meta:
        model = Pacientes
        fields = ('historial', 'id')
        widgets = {'historial': forms.Textarea}


class PacientesForm(forms.ModelForm):
    class Meta:
        model = Pacientes
        fields = ('id','nombre','apellido')
        widgets = {
            'nombre': forms.TextInput(attrs = {'class':'form-control'}),
            'apellido': forms.TextInput(attrs = {'class':'form-control'})
        }
