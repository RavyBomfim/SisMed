from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from cadastros.models import Funcionario, Medico

class UsuarioForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 8:
            raise forms.ValidationError('A senha deve ter pelo menos 8 caracteres.')
        if not any(char.isdigit() for char in password1):
            raise forms.ValidationError('A senha deve conter pelo menos um número.')
        if not any(char.isalpha() for char in password1):
            raise forms.ValidationError('A senha deve conter pelo menos uma letra.')
        
        return password1
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 != password2:
            raise forms.ValidationError('*As senhas não coincidem.')

        return password2


class UsuarioFormEdit(forms.ModelForm):
    email = forms.EmailField(max_length=100)
    class Meta:
        model = User
        fields = ['username']


class SenhaFormEdit(forms.ModelForm):
    password1 = forms.CharField(
        label="Nova Senha",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    password2 = forms.CharField(
        label="Confirme a Senha",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = User
        fields = []

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 != password2:
            raise forms.ValidationError("As senhas não correspondem.")
        return password2

    def save(self, commit=True):
        user = super(SenhaFormEdit, self).save(commit=False)
        password = self.cleaned_data["password1"]
        user.set_password(password)
        if commit:
            user.save()
        return user