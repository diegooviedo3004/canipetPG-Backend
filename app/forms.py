from django import forms
from .models import (Paciente, client, Citas, Product)
from crispy_forms.layout import Submit
from crispy_forms.helper import FormHelper
from django.utils import timezone
from django_select2.forms import Select2MultipleWidget

class ClientForm(forms.ModelForm):
    class Meta:
        model = client
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args, **kwargs)
        for i in self.fields:
            self.fields[i].widget.attrs.update({'class': 'form-control'})

class PacienteForm(forms.ModelForm):
    
    class Meta:
        model = Paciente
        fields = '__all__'

    def __init__(self,  *args, **kwargs):
        super(PacienteForm, self).__init__(*args, **kwargs)
        self.fields['peso'].widget.attrs['placeholder'] = 'Kg'

        self.helper = FormHelper(self)
        self.helper.add_input(Submit('submit', 'Enviar'))
        self.fields['fecha_nacimiento'].widget = forms.DateInput(attrs={'type' : 'date'})

class CitasForm(forms.ModelForm):
    
    class Meta:
        model = Citas
        exclude = ('user',)

    def __init__(self,  *args, **kwargs):
        super(CitasForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.fields['fecha_cita'].widget = forms.DateInput(attrs={'type' : 'date', 'min': timezone.now().date().strftime('%Y-%m-%d')}) 
        self.fields['hora'].widget =  forms.TimeInput(attrs={'type': 'time'})                                                                                                                                                                                                                                                                                                                     
        self.helper.add_input(Submit('submit', 'Enviar'))   

class ProductForm(forms.ModelForm):
    
    class Meta:
        model = Product
        exclude = ('user',)
    
        widgets = {
            'promocionar_a': Select2MultipleWidget,
        }

    def __init__(self,  *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['precio'].widget.attrs['placeholder'] = 'C$'
        self.fields['descuento'].widget.attrs['placeholder'] = 'Porcentaje(%)'
        self.helper = FormHelper(self)
        self.helper.add_input(Submit('submit', 'Enviar'))

