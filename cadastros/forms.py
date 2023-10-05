from django import forms
from .models import Cargo, Endereco, Especialidade, Funcionario, Medico, Paciente

class EnderecoForm(forms.ModelForm):
    class Meta:
        model = Endereco
        fields = ['rua', 'numero', 'bairro', 'cidade']


class MedicoForm(forms.ModelForm):
    especialidade = forms.ModelChoiceField(queryset=Especialidade.objects.all(), empty_label="Selecione uma especialidade")
     
    class Meta:
        model = Medico
        fields = ['nome_completo', 'data_nascimento', 'rg', 'cpf', 'telefone', 'email', 'data_cadastro', 'especialidade', 'foto']
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'class': 'data-mask'}),
            'rg': forms.TextInput(attrs={'class': 'rg-mask'}),
            'cpf': forms.TextInput(attrs={'class': 'cpf-mask'}),
            'telefone': forms.TextInput(attrs={'class': 'telefone-mask'}),
            'data_cadastro': forms.DateInput(attrs={'class': 'data-mask'}),
        }

    endereco = EnderecoForm()


class FuncionarioForm(forms.ModelForm):
    cargo = forms.ModelChoiceField(queryset=Cargo.objects.all(), empty_label="Selecione um cargo", to_field_name='id', label='Cargo'  )
     
    class Meta:
        model = Funcionario
        fields = ['nome_completo', 'data_nascimento', 'rg', 'cpf', 'telefone', 'email', 'data_cadastro', 'cargo', 'foto']
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'class': 'data-mask'}),
            'rg': forms.TextInput(attrs={'class': 'rg-mask'}),
            'cpf': forms.TextInput(attrs={'class': 'cpf-mask'}),
            'telefone': forms.TextInput(attrs={'class': 'telefone-mask'}),
            'data_cadastro': forms.DateInput(attrs={'class': 'data-mask'}),
        }

    endereco = EnderecoForm()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Configurar a representação do campo de seleção de cargo
        self.fields['cargo'].label_from_instance = lambda obj: obj.nome_cargo


class PacienteForm(forms.ModelForm):
     
    class Meta:
        model = Paciente
        fields = ['nome_completo', 'data_nascimento', 'rg', 'cpf', 'telefone', 'email', 'data_cadastro', 'informacoes_medicas', 'foto']
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'class': 'data-mask'}),
            'rg': forms.TextInput(attrs={'class': 'rg-mask'}),
            'cpf': forms.TextInput(attrs={'class': 'cpf-mask'}),
            'telefone': forms.TextInput(attrs={'class': 'telefone-mask'}),
            'data_cadastro': forms.DateInput(attrs={'class': 'data-mask'}),
        }

    endereco = EnderecoForm()