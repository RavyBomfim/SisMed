from django import forms
from .models import Cargo, Endereco, Especialidade, Funcionario, HorarioMedico, Medico, Paciente, sexo_opcoes

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
            'foto' :forms.ClearableFileInput(attrs={'class': 'foto'})
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
    class Meta:
        model = HorarioMedico
        fields = ['dia_semana', 'horario_inicial_manha', 'horario_final_manha', 'horario_inicial_tarde', 'horario_final_tarde']

    def __init__(self, *args, **kwargs):
        super(HorarioMedicoForm, self).__init__(*args, **kwargs)
        self.fields['dia_semana'].widget = forms.Select(choices=HorarioMedico.dias_opcoes)


class AgendamentoConsulta(forms.ModelForm):
    paciente = forms.ModelChoiceField(queryset=Cargo.objects.all(), empty_label="Selecione o paciente",widget=forms.Select(attrs={'class': 'select'}))
    paciente = forms.ModelChoiceField(queryset=Cargo.objects.all(), empty_label="Selecione o medico",widget=forms.Select(attrs={'class': 'select'}))

    class Meta:
        model = HorarioMedico
        fields = '__all__'
        widgets = {
            'data_hora': forms.DateTimeInput(attrs={'type': 'datetime', 'class': 'data-mask'}),
            'rg': forms.TextInput(attrs={'class': 'rg-mask'}),
            'cpf': forms.TextInput(attrs={'class': 'cpf-mask'}),
        }