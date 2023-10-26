from datetime import datetime
from django import forms
from cadastros.models import Medico, AgendamentoConsulta, Paciente, boolean_opcoes, tipo_consulta_opcoes

class AgendamentoConsultaForm(forms.ModelForm):
    paciente = forms.ModelChoiceField(queryset=Paciente.objects.all(), empty_label="Selecionar Paciente")
    medico = forms.ModelChoiceField(queryset=Medico.objects.all(), empty_label="Selecionar Médico/Especialidade", widget=forms.Select(attrs={'class': 'select'}))
    data = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    horario = forms.CharField(widget=forms.Select(attrs={'class': 'select'}))
    tipo_consulta = forms.ChoiceField(choices=[('', 'Plano/Particular?')] + list(tipo_consulta_opcoes))
    retorno = forms.ChoiceField(choices=[('', 'Retorno?')] + list(boolean_opcoes), widget=forms.Select)
    """tipo_consulta = forms.ChoiceField(choices=tipo_consulta_opcoes, widget=forms.RadioSelect(attrs={'class': 'with-gap'}))
    retorno = forms.BooleanField(label='Retorno', required=False, widget=forms.RadioSelect(choices=boolean_opcoes))"""
    valor_consulta = forms.DecimalField(label='Valor da Consulta')

    class Meta:
        model = AgendamentoConsulta
        fields = ['data', 'horario', 'paciente', 'medico', 'tipo_consulta', 'retorno', 'valor_consulta']


    def clean_horario(self):
        horario_str = self.cleaned_data['horario']
        try:
            horario_str += ':00'
            horario = datetime.strptime(horario_str, '%H:%M:%S').time()
            return horario
        except ValueError:
            raise forms.ValidationError("Formato de horário inválido. Use HH:MM")

    

