from datetime import datetime
from django import forms
from cadastros.models import Atendimento, Medico, Agendamento, Paciente, Procedimento, tipo_agendamento_opcoes, boolean_opcoes, tipo_pagamento_opcoes

class AgendamentoForm(forms.ModelForm):
    tipo_agendamento = forms.ChoiceField(choices=tipo_agendamento_opcoes, widget=forms.RadioSelect(attrs={'class': 'with-gap'}), initial='Consulta')
    procedimento = forms.ModelChoiceField(queryset=Procedimento.objects.all(), empty_label="Selecionar Procedimento", widget=forms.Select(attrs={'class': 'select'}), required=False)
    paciente = forms.ModelChoiceField(queryset=Paciente.objects.all(), empty_label="Selecionar Paciente", widget=forms.Select(attrs={'class': 'select'}))
    medico = forms.ModelChoiceField(queryset=Medico.objects.all(), empty_label="Selecionar Médico/Especialidade", widget=forms.Select(attrs={'class': 'select'}))
    data = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    horario = forms.CharField(widget=forms.Select(attrs={'class': 'select'}))
    tipo_pagamento = forms.ChoiceField(choices=[('', 'Plano/Particular?')] + list(tipo_pagamento_opcoes), widget=forms.Select(attrs={'class': 'select'}))
    retorno = forms.ChoiceField(choices=[('', 'Retorno?')] + list(boolean_opcoes), widget=forms.Select(attrs={'class': 'select'}), required=False)
    valor = forms.DecimalField(label='Valor da Consulta')

    class Meta:
        model = Agendamento
        fields = ['tipo_agendamento','procedimento','data', 'horario', 'paciente', 'medico', 'tipo_pagamento', 'retorno', 'valor']

    def clean_horario(self):
        horario_str = self.cleaned_data['horario']
        try:
            horario_str += ':00'
            horario = datetime.strptime(horario_str, '%H:%M:%S').time()
            return horario
        except ValueError:
            raise forms.ValidationError("Formato de horário inválido. Use HH:MM")
    

class AtendimentoForm(forms.ModelForm):
    class Meta:
        model = Atendimento
        fields = ['consulta', 'anamnese_paciente', 'diagnostico', 'receituario']