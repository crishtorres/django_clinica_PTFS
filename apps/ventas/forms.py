from django import forms
from .models import PedidosCab, PedidosDet, Productos

class PedidosForm(forms.ModelForm):

    class Meta:
        model = PedidosCab
        fields = ('id','paciente', 'fecha','pago')

        widgets = {
            'fecha': forms.DateInput(attrs={'class':'form-control', 'type': 'date'}),
            'paciente': forms.Select(attrs={'class':'form-control'}),
            'pago': forms.Select(attrs={'class': 'form-control'})
        }


class PedidosDetForm(forms.ModelForm):

    class Meta:
        model = PedidosDet
        fields = ('id', 'producto', 'cantidad', 'unitario', 'clasificacion', 'cercania', 'lado', 'armazon')

        widgets = {
            'cantidad': forms.NumberInput(attrs={'class':'form-control'}),
            'unitario': forms.NumberInput(attrs={'class': 'form-control'}),
            'producto': forms.Select(attrs={'class': 'form-control'}),
            'clasificacion': forms.Select(attrs={'class': 'form-control'}),
            'cercania': forms.Select(attrs={'class': 'form-control'}),
            'lado': forms.Select(attrs={'class': 'form-control'}),
            'armazon': forms.Select(attrs={'class': 'form-control'}),
        }

class StatusForm(forms.ModelForm):

    class Meta:
        OPT_ESTADOS = (
            ('P', 'Pendiente'),
            ('O', 'Pedido'),
            ('T', 'Taller'),
        )

        model = PedidosCab
        fields = ('estado', 'id')
        widgets = {'estado': forms.Select(attrs = {'class' : 'form-control'}, choices = OPT_ESTADOS)}

class ProductosForm(forms.ModelForm):
    class Meta:
        model = Productos
        fields = '__all__'
        widgets = {
            'codigo': forms.TextInput(attrs={'class':'form-control'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'clasificacion': forms.Select(attrs={'class': 'form-control'}),
        }