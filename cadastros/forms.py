from django import forms
from .models import Cargo, Endereco, Especialidade, Funcionario, HorarioMedico, Medico, Paciente, Procedimento, sexo_opcoes, dias_semana_opcoes

class EnderecoForm(forms.ModelForm):
    class Meta:
        model = Endereco
        fields = ['rua', 'numero', 'bairro', 'cidade']


class MedicoForm(forms.ModelForm):
    especialidade = forms.ModelChoiceField(queryset=Especialidade.objects.all(), empty_label="Selecione uma especialidade", widget=forms.Select(attrs={'class': 'select'}))
    sexo = forms.ChoiceField(choices=[('', 'Selecione um sexo')] + list(sexo_opcoes))
     
    class Meta:
        model = Medico
        fields = ['nome_completo', 'data_nascimento', 'rg', 'cpf', 'crm', 'sexo', 'telefone', 'email', 'especialidade', 'foto']
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date', 'class': 'data-mask'}),
            'rg': forms.TextInput(attrs={'class': 'rg-mask'}),
            'cpf': forms.TextInput(attrs={'class': 'cpf-mask'}),
            'crm': forms.TextInput(attrs={'class': 'crm-mask'}),
            'telefone': forms.TextInput(attrs={'class': 'telefone-mask'}),
        }

    endereco = EnderecoForm()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Configurar a representação do campo de seleção de cargo
        self.fields['especialidade'].label_from_instance = lambda obj: obj.especialidade


class FuncionarioForm(forms.ModelForm):
    cargo = forms.ModelChoiceField(queryset=Cargo.objects.all(), empty_label="Selecione um cargo",widget=forms.Select(attrs={'class': 'select'}))
    sexo = forms.ChoiceField(choices=[('', 'Selecione um sexo')] + list(sexo_opcoes))
     
    class Meta:
        model = Funcionario
        fields = ['nome_completo', 'data_nascimento', 'rg', 'cpf', 'sexo', 'data_admissao', 'data_demissao', 'telefone', 'email', 'cargo', 'foto']
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date', 'class': 'data-mask'}),
            'rg': forms.TextInput(attrs={'class': 'rg-mask'}),
            'cpf': forms.TextInput(attrs={'class': 'cpf-mask'}),
            'telefone': forms.TextInput(attrs={'class': 'telefone-mask'}),
            'data_admissao': forms.DateInput(attrs={'class': 'data-mask'}),
            'data_demissao': forms.DateInput(attrs={'class': 'data-mask'}),
        }

    endereco = EnderecoForm()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Configurar a representação do campo de seleção de cargo
        self.fields['cargo'].label_from_instance = lambda obj: obj.nome_cargo


class PacienteForm(forms.ModelForm):
    sexo = forms.ChoiceField(choices=[('', 'Selecione um sexo')] + list(sexo_opcoes))
     
    class Meta:
        model = Paciente
        fields = ['nome_completo', 'data_nascimento', 'rg', 'cpf', 'sexo', 'telefone', 'email', 'informacoes_medicas', 'foto']
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date', 'class': 'data-mask'}),
            'rg': forms.TextInput(attrs={'class': 'rg-mask'}),
            'cpf': forms.TextInput(attrs={'class': 'cpf-mask'}),
            'telefone': forms.TextInput(attrs={'class': 'telefone-mask'}),
        }

    endereco = EnderecoForm()


class HorarioMedicoForm(forms.ModelForm):
    dia_semana = forms.ChoiceField(choices=[('', 'Selecione o dia da Semana')] + list(dias_semana_opcoes))

    class Meta:
        model = HorarioMedico
        fields = ['agenda', 'dia_semana', 'horario_inicial_manha', 'horario_final_manha', 'horario_inicial_tarde', 'horario_final_tarde']

    def clean(self):
        cleaned_data = super().clean()
        agenda = cleaned_data.get('agenda')
        dia_semana = cleaned_data.get('dia_semana')
        horario_inicial_manha = cleaned_data.get('horario_inicial_manha')
        horario_final_manha = cleaned_data.get('horario_final_manha')
        horario_inicial_tarde = cleaned_data.get('horario_inicial_tarde')
        horario_final_tarde = cleaned_data.get('horario_final_tarde')

        if HorarioMedico.objects.filter(agenda=agenda, dia_semana=dia_semana).exclude(pk=self.instance.pk).exists():
            self.add_error('dia_semana', "Este dia já está cadastrado nesta agenda.")

        if not horario_inicial_manha and not horario_final_manha and not horario_inicial_tarde and not horario_final_tarde:
            self.add_error('horario_inicial_tarde', 'Cadastre pelo menos um período de horário.')
        else:
            if horario_inicial_manha and horario_final_manha:
                if horario_inicial_manha >= horario_final_manha:
                    self.add_error('horario_inicial_manha', 'O horário inicial não pode ser maior ou igual ao horário final.')
            else:
                if not horario_inicial_manha and horario_final_manha:
                    self.add_error('horario_inicial_manha', 'Preencha o horário inicial para o período da manhã.')
                elif horario_inicial_manha and not horario_final_manha:
                    self.add_error('horario_final_manha', 'Preencha o horário final para o período da manhã.')

            if horario_inicial_tarde and horario_final_tarde:
                if horario_inicial_tarde >= horario_final_tarde:
                    self.add_error('horario_inicial_tarde', 'O horário inicial não pode ser maior ou igual ao horário final.')
            else:
                if not horario_inicial_tarde and horario_final_tarde:
                    self.add_error('horario_inicial_tarde', 'Preencha o horário inicial para o período da tarde.')
                elif horario_inicial_tarde and not horario_final_tarde:
                    self.add_error('horario_final_tarde', 'Preencha o horário final para o período da tarde.')


class ProcedimentoForm(forms.ModelForm):
    especialidade_responsavel = forms.ModelChoiceField(queryset=Especialidade.objects.all(), empty_label="Selecionar Especialidade", widget=forms.Select(attrs={'class': 'select'}),
    required=False)
    valor_procedimento = forms.DecimalField(max_digits=8, decimal_places=2,
        widget=forms.TextInput(attrs={'class': 'preco'}))

    class Meta:
        model = Procedimento
        fields = ['nome_procedimento', 'especialidade_responsavel', 'descricao', 'valor_procedimento']


"""class AgendamentoConsulta(forms.ModelForm):
    paciente = forms.ModelChoiceField(queryset=Cargo.objects.all(), empty_label="Selecione o paciente",widget=forms.Select(attrs={'class': 'select'}))
    paciente = forms.ModelChoiceField(queryset=Cargo.objects.all(), empty_label="Selecione o medico",widget=forms.Select(attrs={'class': 'select'}))

    class Meta:
        model = HorarioMedico
        fields = '__all__'
        widgets = {
            'data_hora': forms.DateTimeInput(attrs={'type': 'datetime', 'class': 'data-mask'}),
            'rg': forms.TextInput(attrs={'class': 'rg-mask'}),
            'cpf': forms.TextInput(attrs={'class': 'cpf-mask'}),
        }"""