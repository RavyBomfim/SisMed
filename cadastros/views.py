from typing import Any
from .forms import EnderecoForm, FuncionarioForm, MedicoForm, PacienteForm
from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import  ListView
from django.views.generic.detail import DetailView
from .models import Cargo, Funcionario, Especialidade, Medico, Paciente, Endereco
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import GroupRequiredMixin
from django.shortcuts import get_object_or_404

# Create your views here.

# --------------- Views de Cadastro ---------------

class CargoCreate(CreateView, LoginRequiredMixin, GroupRequiredMixin):
    login_url = reverse_lazy('login')
    group_required = u"Administrador"
    model = Cargo
    fields = ['nome_cargo', 'salario']
    template_name = 'cadastros/form.html'
    success_url = reverse_lazy('listar-cargos')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = 'Cadastro de Cargos'

        return context


class FuncionarioCreate(CreateView, LoginRequiredMixin, GroupRequiredMixin):
    login_url = reverse_lazy('login')
    group_required = u"Administrador"
    model = Funcionario
    form_class = FuncionarioForm
    template_name = 'cadastros/form_funcionario.html'
    success_url = reverse_lazy('listar-funcionarios')


    def form_valid(self, form):
        funcionario = form.save(commit=False)
        endereco_form = EnderecoForm(self.request.POST)

        if endereco_form.is_valid():
            endereco = endereco_form.save(commit=False)
            endereco.save()

            funcionario.endereco = endereco
            funcionario.save()
            return super().form_valid(form)


    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titulo'] = 'Cadastro de Funcionários'
        return context


class EspecialidadeCreate(CreateView, LoginRequiredMixin, GroupRequiredMixin):
    login_url = reverse_lazy('login')
    group_required = u"Administrador"
    model = Especialidade
    fields = ['especialidade']
    template_name = 'cadastros/form.html'
    success_url = reverse_lazy('listar-especialidades')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = 'Cadastro de Especialidades'

        return context


class MedicoCreate(CreateView, LoginRequiredMixin, GroupRequiredMixin):
    model = Medico
    form_class = MedicoForm
    template_name = 'cadastros/form_medico.html'
    success_url = reverse_lazy('listar-medicos')

    def form_valid(self, form):
        # Criando o objeto Medico a partir do MedicoForm
        medico = form.save(commit=False)
        # Criando uma instância do sub-formulário EnderecoForm e preenchendo com os dados do request
        endereco_form = EnderecoForm(self.request.POST)

        # Verificando se o EnderecoForm é válido
        if endereco_form.is_valid():
            # Salvando o objeto Endereco para obter um ID
            endereco = endereco_form.save(commit=False)
            endereco.save()
            # Criando o objeto Endereco a partir do EnderecoForm
            medico.endereco = endereco
            medico.save()
            return super().form_valid(form)
        

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = 'Cadastro de Médicos'

        return context
    

class PacienteCreate(CreateView, LoginRequiredMixin, GroupRequiredMixin):
    login_url = reverse_lazy('login')
    group_required = u"Administrador"
    model = Paciente
    form_class = PacienteForm
    template_name = 'cadastros/form_paciente.html'
    success_url = reverse_lazy('listar-pacientes')


    def form_valid(self, form):
        paciente = form.save(commit=False)
        endereco_form = EnderecoForm(self.request.POST)

        if endereco_form.is_valid():
            endereco = endereco_form.save(commit=False)
            endereco.save()

            paciente.endereco = endereco
            paciente.save()
            return super().form_valid(form)


    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = 'Cadastro de Pacientes'

        return context
    


# --------------- Views de Edição ---------------

class CargoUpdate(UpdateView, LoginRequiredMixin, GroupRequiredMixin):
    login_url = reverse_lazy('login')
    group_required = u"Administrador"
    model = Cargo
    fields = ['nome_cargo', 'salario']
    template_name = 'cadastros/form.html'
    success_url = reverse_lazy('listar-cargos')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = 'Editar Dados'

        return context


class FuncionarioUpdate(UpdateView, LoginRequiredMixin, GroupRequiredMixin):
    login_url = reverse_lazy('login')
    group_required = u"Administrador"
    model = Funcionario
    form_class = FuncionarioForm
    template_name = 'cadastros/form_funcionario.html'
    success_url = reverse_lazy('listar-funcionarios')


    def form_valid(self, form):
        funcionario = get_object_or_404(Funcionario, pk=self.kwargs['pk'])

        if funcionario.endereco: 
            funcionario.endereco.rua = self.request.POST['rua']
            funcionario.endereco.numero = self.request.POST['numero']
            funcionario.endereco.bairro = self.request.POST['bairro']
            funcionario.endereco.cidade = self.request.POST['cidade']
        else:
            endereco_form = EnderecoForm(self.request.POST)
            if endereco_form.is_valid():
                endereco = endereco_form.save(commit=False)
                endereco.save()
                funcionario.endereco = endereco

        funcionario.endereco.save()

        return super().form_valid(form)


    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        if self.object:
            funcionario = self.object
            endereco_inicial = {
                'rua': funcionario.endereco.rua if funcionario.endereco else '',
                'numero': funcionario.endereco.numero if funcionario.endereco else '',
                'bairro': funcionario.endereco.bairro if funcionario.endereco else '',
                'cidade': funcionario.endereco.cidade if funcionario.endereco else '',
            }

            context['endereco_inicial'] = endereco_inicial

        context['titulo'] = 'Editar Dados de Funcionário'

        return context


class EspecialidadeUpdate(UpdateView, LoginRequiredMixin, GroupRequiredMixin):
    login_url = reverse_lazy('login')
    group_required = u"Administrador"
    model = Especialidade
    fields = ['especialidade']
    template_name = 'cadastros/form.html'
    success_url = reverse_lazy('listar-especialidades')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = 'Editar Dados'

        return context

class MedicoUpdate(UpdateView, LoginRequiredMixin, GroupRequiredMixin):
    login_url = reverse_lazy('login')
    group_required = u"Administrador"
    model = Medico
    form_class = MedicoForm   
    template_name = 'cadastros/form_medico.html'
    success_url = reverse_lazy('listar-medicos')
    

    def form_valid(self, form):
        medico = get_object_or_404(Medico, pk=self.kwargs['pk'])

        if medico.endereco: 
            medico.endereco.rua = self.request.POST['rua']
            medico.endereco.numero = self.request.POST['numero']
            medico.endereco.bairro = self.request.POST['bairro']
            medico.endereco.cidade = self.request.POST['cidade']
        else:
            endereco_form = EnderecoForm(self.request.POST)
            if endereco_form.is_valid():
                endereco = endereco_form.save(commit=False)
                endereco.save()
                medico.endereco = endereco

        medico.endereco.save()

        return super().form_valid(form)
    

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        if self.object:
            medico = self.object
            endereco_inicial = {
                'rua': medico.endereco.rua if medico.endereco else '',
                'numero': medico.endereco.numero if medico.endereco else '',
                'bairro': medico.endereco.bairro if medico.endereco else '',
                'cidade': medico.endereco.cidade if medico.endereco else '',
            }

            # Adicione o dicionário ao contexto
            context['endereco_inicial'] = endereco_inicial

        context['titulo'] = 'Editar Dados de Médico'

        return context


class PacienteUpdate(UpdateView, LoginRequiredMixin, GroupRequiredMixin):
    login_url = reverse_lazy('login')
    group_required = u"Administrador"
    model = Paciente
    form_class = PacienteForm
    template_name = 'cadastros/form_paciente.html'
    success_url = reverse_lazy('listar-pacientes')


    def form_valid(self, form):
        paciente = get_object_or_404(Paciente, pk=self.kwargs['pk'])

        if paciente.endereco: 
            paciente.endereco.rua = self.request.POST['rua']
            paciente.endereco.numero = self.request.POST['numero']
            paciente.endereco.bairro = self.request.POST['bairro']
            paciente.endereco.cidade = self.request.POST['cidade']
        else:
            endereco_form = EnderecoForm(self.request.POST)
            if endereco_form.is_valid():
                endereco = endereco_form.save(commit=False)
                endereco.save()
                paciente.endereco = endereco

        paciente.endereco.save()

        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        if self.object:
            paciente = self.object
            endereco_inicial = {
                'rua': paciente.endereco.rua if paciente.endereco else '',
                'numero': paciente.endereco.numero if paciente.endereco else '',
                'bairro': paciente.endereco.bairro if paciente.endereco else '',
                'cidade': paciente.endereco.cidade if paciente.endereco else '',
            }

            context['endereco_inicial'] = endereco_inicial

        context['titulo'] = 'Editar Dados de Paciente'

        return context


# --------------- Views para excluir  ---------------

class CargoDelete(DeleteView, LoginRequiredMixin, GroupRequiredMixin):
    login_url = reverse_lazy('login')
    group_required = u"Administrador"
    model = Cargo
    template_name = 'cadastros/form_excluir.html'
    success_url = reverse_lazy('listar-cargos')

class FuncionarioDelete(DeleteView, LoginRequiredMixin, GroupRequiredMixin):
    login_url = reverse_lazy('login')
    group_required = u"Administrador"
    model = Funcionario
    template_name = 'cadastros/form_excluir.html'
    success_url = reverse_lazy('listar-funcionarios')


class EspecialidadeDelete(DeleteView,LoginRequiredMixin, GroupRequiredMixin):
    login_url = reverse_lazy('login')
    group_required = u"Administrador"
    model = Especialidade
    template_name = 'cadastros/form_excluir.html'
    success_url = reverse_lazy('listar-especialidades')


class MedicoDelete(DeleteView, LoginRequiredMixin, GroupRequiredMixin):
    login_url = reverse_lazy('login')
    group_required = u"Administrador"
    model = Medico
    template_name = 'cadastros/form_excluir.html'
    success_url = reverse_lazy('listar-medicos')


class PacienteDelete(DeleteView, LoginRequiredMixin, GroupRequiredMixin):
    login_url = reverse_lazy('login')
    group_required = u"Administrador"
    model = Paciente
    template_name = 'cadastros/form_excluir.html'
    success_url = reverse_lazy('listar-pacientes')

# --------------- Views para Listar ---------------

class CargoList(ListView, LoginRequiredMixin, GroupRequiredMixin):
    login_url = reverse_lazy('login')
    model = Cargo
    template_name = 'cadastros/listas/cargo.html'
    success_url = reverse_lazy('inicio')


class FuncionarioList(ListView, LoginRequiredMixin):
    login_url = reverse_lazy('login')
    model = Funcionario
    template_name = 'cadastros/listas/funcionario.html'
    success_url = reverse_lazy('inicio')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
    
        context['titulo'] = 'Funcionários'

        return context


class EspecialidadeList(ListView, LoginRequiredMixin, GroupRequiredMixin):
    login_url = reverse_lazy('login')
    model = Especialidade
    template_name = 'cadastros/listas/especialidade.html'
    success_url = reverse_lazy('listar-especialidades')


class MedicoList(ListView, LoginRequiredMixin):
    login_url = reverse_lazy('login')
    model = Medico
    template_name = 'cadastros/listas/medico.html'
    success_url = reverse_lazy('listar-medicos')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
    
        context['titulo'] = 'Médicos'

        return context


class PacienteList(ListView, LoginRequiredMixin):
    login_url = reverse_lazy('login')
    model = Paciente
    template_name = 'cadastros/listas/paciente.html'
    success_url = reverse_lazy('listar-pacientes')


    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['titulo'] = 'Pacientes'

        return context


# --------------- Views para Detalhar dados ---------------
class FuncionarioDetail(DetailView):
    model = Funcionario
    template_name = 'cadastros/listas/dados_funcionario.html'
    context_object_name = 'funcionario'


class MedicoDetail(DetailView):
    model = Medico
    template_name = 'cadastros/listas/dados_medico.html'
    context_object_name = 'medico'


class PacienteDetail(DetailView):
    model = Paciente
    template_name = 'cadastros/listas/dados_paciente.html'
    context_object_name = 'paciente'