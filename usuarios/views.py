from django.dispatch import receiver
from django.db.models.signals import post_save
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import  ListView
from django.contrib.auth.models import User, Group
from cadastros.models import Medico
from paginas.views import GrupoMixin
from .forms import SenhaFormEdit, UsuarioForm, UsuarioFormEdit
from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import GroupRequiredMixin
from django.shortcuts import get_object_or_404

# Create your views here.

# --------------- Views de Cadastro ---------------

class UsuarioCreate(GroupRequiredMixin, LoginRequiredMixin, GrupoMixin, CreateView):
    login_url = reverse_lazy('login')
    group_required = u'Administrador'
    form_class = UsuarioForm
    template_name = 'usuarios/form_usuario.html'
    success_url = reverse_lazy('listar-usuarios')

    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = 'Cadastro de Usuário'

        return context
 

@receiver(post_save, sender=User)
def associar_usuario_a_medico(sender, instance, created, **kwargs):
    if created:
        medico = Medico.objects.latest('id')
        if medico:
            medico.usuario = instance
            medico.save()
            grupo_medico, _ = Group.objects.get_or_create(name='Medico')
            instance.groups.add(grupo_medico)


# --------------- Views para Edição ---------------

class UsuarioUpdate(LoginRequiredMixin, GrupoMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = User
    form_class = UsuarioFormEdit
    template_name = 'usuarios/edit_usuario.html'
    success_url = reverse_lazy('listar-usuarios')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = 'Editar Usuário'

        return context
    

class SenhaUpdate(LoginRequiredMixin, GrupoMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = User
    form_class = SenhaFormEdit
    template_name = 'usuarios/senha_edit.html'
    success_url = reverse_lazy('listar-usuarios')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = 'Editar Senha'

        return context
    

# --------------- Views para Excluir ---------------

class UsuarioDelete(GroupRequiredMixin, LoginRequiredMixin, GrupoMixin, DeleteView):
    login_url = 'login'
    group_required = u'Administrador'
    model = User
    template_name = 'cadastros/form_excluir.html'
    success_url = reverse_lazy('listar-usuarios')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['objeto'] = 'o usuário'
        obj = self.get_object()
        context['registro'] = obj.username
        return context
    

# --------------- Views para Listar ---------------

class UsuarioList(GroupRequiredMixin, LoginRequiredMixin, GrupoMixin, ListView):
    login_url = reverse_lazy('login')
    group_required = u'Administrador'
    model = User
    template_name = 'usuarios/lista/usuario.html'
    success_url = reverse_lazy('listar-usuarios')


class MeusPacientes(GroupRequiredMixin, LoginRequiredMixin, GrupoMixin, ListView):
    login_url = reverse_lazy('login')
    group_required = u'Medico'
    model = User
    template_name = 'usuarios/lista/usuario.html'
    success_url = reverse_lazy('listar-usuarios')