from typing import Any
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import  ListView
from django.contrib.auth.models import User, Group
from .forms import UsuarioForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404

# Create your views here.
class UsuarioCreate(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    form_class = UsuarioForm
    template_name = 'usuarios/form_usuario.html'
    success_url = reverse_lazy('listar-usuarios')

    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = 'Cadastro de Novo Usuário'

        return context
    

    """def form_valid(self, form):

        grupo = get_object_or_404(Group, name='Administrador')

        url = super().form_valid(form)

        self.object.groups.add(grupo)

        return url"""
    

class UsuarioList(ListView):
    login_url = reverse_lazy('login')
    model = User
    template_name = 'usuarios/lista/usuario.html'
    success_url = reverse_lazy('listar-usuarios')