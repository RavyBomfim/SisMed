from paginas.views import GrupoMixin
from .forms import EnderecoForm, FuncionarioForm, HorarioMedicoForm, MedicoForm, PacienteForm, ProcedimentoForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import AgendaMedico, Cargo, Funcionario, Especialidade, HorarioMedico, Medico, Paciente, Procedimento, Prontuario, dias_semana_opcoes
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import GroupRequiredMixin
from django.shortcuts import get_object_or_404
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your views here.

# --------------- Views de Cadastro ---------------
class CargoCreate(GroupRequiredMixin, LoginRequiredMixin, GrupoMixin, CreateView):
    login_url = reverse_lazy('login')
    group_required = u'Administrador'
    model = Cargo
    fields = ['nome_cargo', 'salario']
    template_name = 'cadastros/form.html'
    success_url = reverse_lazy('listar-cargos')
    

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['form'].fields['salario'].widget.attrs['class'] = 'preco'
        context['titulo'] = 'Cadastro de Cargos'

        return context


class FuncionarioCreate(GroupRequiredMixin, LoginRequiredMixin, GrupoMixin, CreateView):
    login_url = reverse_lazy('login')
    group_required = u'Administrador'
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


class EspecialidadeCreate(GroupRequiredMixin, LoginRequiredMixin, GrupoMixin, CreateView):
    login_url = reverse_lazy('login')
    group_required = u'Administrador'
    model = Especialidade
    fields = ['especialidade', 'valor_consulta']
    template_name = 'cadastros/form.html'
    success_url = reverse_lazy('listar-especialidades')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['form'].fields['valor_consulta'].widget.attrs['class'] = 'preco'
        context['titulo'] = 'Cadastro de Especialidades'

        return context


class MedicoCreate(GroupRequiredMixin, LoginRequiredMixin, GrupoMixin, CreateView):
    login_url = reverse_lazy('login')
    group_required = u'Administrador'
    model = Medico
    form_class = MedicoForm
    template_name = 'cadastros/form_medico.html'
    success_url = reverse_lazy('cadastrar-usuario')

    def form_valid(self, form):
        # Criando o objeto Medico a partir do MedicoForm
        medico = form.save(commit=False)
        # Criando uma instância do sub-formulário EnderecoForm e preenchendo com os dados do request
        endereco_form = EnderecoForm(self.request.POST)

        # Verificando se o EnderecoForm é válido
        if endereco_form.is_valid():
            # Salvando o objeto Endereco para obter um ID
            endereco = endereco_form.save()
            # Criando o objeto Endereco a partir do EnderecoForm
            medico.endereco = endereco
            medico.save()
            return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titulo'] = 'Cadastro de Médicos'
        return context
    
# Signal para criação de agenda do médico
@receiver(post_save, sender=Medico)
def associar_usuario_a_medico(sender, instance, created, **kwargs):
    if created:
        # Criando uma agenda e associando ao médico recém criado
        AgendaMedico.objects.create(medico=instance)


class PacienteCreate(GroupRequiredMixin, LoginRequiredMixin, GrupoMixin, CreateView):
    login_url = reverse_lazy('login')
    group_required = u'Administrador'
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


# Signal para criação de prontuário do paciente
@receiver(post_save, sender=Paciente)
def associar_usuario_a_medico(sender, instance, created, **kwargs):
    if created:
        Prontuario.objects.create(paciente=instance)


class ProcedimentoCreate(GroupRequiredMixin, LoginRequiredMixin, GrupoMixin, CreateView):
    login_url = reverse_lazy('login')
    group_required = u'Administrador'
    model = Procedimento
    form_class = ProcedimentoForm
    template_name = 'cadastros/form.html'
    success_url = reverse_lazy('listar-procedimentos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Cadastro de Procedimentos'
        return context

# --------------- Views de Edição ---------------

class CargoUpdate(GroupRequiredMixin, LoginRequiredMixin, GrupoMixin, UpdateView):
    login_url = reverse_lazy('login')
    group_required = u'Administrador'
    model = Cargo
    fields = ['nome_cargo', 'salario']
    template_name = 'cadastros/form.html'
    success_url = reverse_lazy('listar-cargos')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['form'].fields['salario'].widget.attrs['class'] = 'preco'
        context['titulo'] = 'Editar Cargo'
        return context


class FuncionarioUpdate(GroupRequiredMixin, LoginRequiredMixin, GrupoMixin, UpdateView):
    login_url = reverse_lazy('login')
    group_required = u'Administrador'
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
            
            foto = {
                'foto': funcionario.foto if funcionario.foto else '',
            }

            context['endereco_inicial'] = endereco_inicial
            context['foto'] = foto

        context['titulo'] = 'Editar Dados de Funcionário'

        return context


class EspecialidadeUpdate(GroupRequiredMixin, LoginRequiredMixin, GrupoMixin, UpdateView):
    login_url = reverse_lazy('login')
    group_required = u'Administrador'
    model = Especialidade
    fields = ['especialidade', 'valor_consulta']
    template_name = 'cadastros/form.html'
    success_url = reverse_lazy('listar-especialidades')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['form'].fields['valor_consulta'].widget.attrs['class'] = 'preco'
        context['titulo'] = 'Editar Especialidade'

        return context


class MedicoUpdate(GroupRequiredMixin, LoginRequiredMixin, GrupoMixin, UpdateView):
    login_url = reverse_lazy('login')
    group_required = u'Administrador'
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

            foto = {
                'foto': medico.foto if medico.foto else '',
            }

            context['endereco_inicial'] = endereco_inicial
            context['foto'] = foto

        context['titulo'] = 'Editar Dados de Médico'
        return context


class PacienteUpdate(GroupRequiredMixin, LoginRequiredMixin, GrupoMixin, UpdateView):
    login_url = reverse_lazy('login')
    group_required = u'Administrador'
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

            foto = {
                'foto': paciente.foto if paciente.foto else '',
            }

            context['endereco_inicial'] = endereco_inicial
            context['foto'] = foto

        context['titulo'] = 'Editar Dados de Paciente'

        return context


class ProcedimentoUpdate(GroupRequiredMixin, LoginRequiredMixin, GrupoMixin, UpdateView):
    login_url = reverse_lazy('login')
    group_required = u'Administrador'
    model = Procedimento
    form_class = ProcedimentoForm
    template_name = 'cadastros/form.html'
    success_url = reverse_lazy('listar-procedimentos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Procedimento'
        return context


# --------------- Views para excluir  ---------------

class CargoDelete(GroupRequiredMixin, LoginRequiredMixin, GrupoMixin, DeleteView):
    login_url = reverse_lazy('login')
    group_required = u'Administrador'
    model = Cargo
    template_name = 'cadastros/form_excluir.html'
    success_url = reverse_lazy('listar-cargos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['objeto'] = 'o cargo'
        obj = self.get_object()  # Obtendo o objeto que será excluído
        context['registro'] = obj.nome_cargo # Adicionando o campo nome_cargo do objeto ao contexto
        return context


class FuncionarioDelete(GroupRequiredMixin, LoginRequiredMixin, GrupoMixin, DeleteView):
    login_url = reverse_lazy('login')
    group_required = u'Administrador'
    model = Funcionario
    template_name = 'cadastros/form_excluir.html'
    success_url = reverse_lazy('listar-funcionarios')

    def delete(self, request, *args, **kwargs):
        funcionario = self.get_object()
        if funcionario.endereco:
            funcionario.endereco.delete()
        if funcionario.usuario:
            funcionario.usuario.delete()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['objeto'] = 'o funcionário'
        obj = self.get_object()
        context['registro'] = obj.nome_completo
        return context


class EspecialidadeDelete(GroupRequiredMixin, LoginRequiredMixin, GrupoMixin, DeleteView):
    login_url = reverse_lazy('login')
    group_required = u'Administrador'
    model = Especialidade
    template_name = 'cadastros/form_excluir.html'
    success_url = reverse_lazy('listar-especialidades')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['objeto'] = 'a especialidade'
        obj = self.get_object()
        context['registro'] = obj.especialidade
        return context


class MedicoDelete(GroupRequiredMixin, LoginRequiredMixin, GrupoMixin, DeleteView):
    login_url = reverse_lazy('login')
    group_required = u'Administrador'
    model = Medico
    template_name = 'cadastros/form_excluir.html'
    success_url = reverse_lazy('listar-medicos')

    def delete(self, request, *args, **kwargs):
        medico = self.get_object()
        # Excluindo o endereço associado ao médico
        if medico.endereco:
            medico.endereco.delete()
        # Excluindo o usuário associado ao médico
        if medico.usuario:
            medico.usuario.delete()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['objeto'] = 'o medico'
        obj = self.get_object()
        context['registro'] = obj.nome_completo
        return context


class PacienteDelete(GroupRequiredMixin, LoginRequiredMixin, GrupoMixin, DeleteView):
    login_url = reverse_lazy('login')
    group_required = u'Administrador'
    model = Paciente
    template_name = 'cadastros/form_excluir.html'
    success_url = reverse_lazy('listar-pacientes')

    def delete(self, request, *args, **kwargs):
        paciente = self.get_object()
        if paciente.endereco:
            paciente.endereco.delete()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['objeto'] = 'o paciente'
        obj = self.get_object()
        context['registro'] = obj.nome_completo
        return context


class ProcedimentoDelete(GroupRequiredMixin, LoginRequiredMixin, GrupoMixin, DeleteView):
    login_url = reverse_lazy('login')
    group_required = u'Administrador'
    model = Procedimento
    template_name = 'cadastros/form_excluir.html'
    success_url = reverse_lazy('listar-procedimentos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['objeto'] = 'o procedimento'
        obj = self.get_object()  # Obtendo o objeto que será excluído
        context['registro'] = obj.nome_procedimento # Adicionando o campo nome_cargo do objeto ao contexto
        return context


# --------------- Views para Listar ---------------

class CargoList(GroupRequiredMixin, LoginRequiredMixin, GrupoMixin, ListView):
    login_url = reverse_lazy('login')
    group_required = u'Administrador'
    model = Cargo
    template_name = 'cadastros/listas/cargo.html'
    success_url = reverse_lazy('inicio')


class FuncionarioList(GroupRequiredMixin, LoginRequiredMixin, GrupoMixin, ListView):
    login_url = reverse_lazy('login')
    group_required = u'Administrador'
    model = Funcionario
    template_name = 'cadastros/listas/funcionario.html'
    success_url = reverse_lazy('inicio')
    

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
    
        context['titulo'] = 'Funcionários'

        return context


class EspecialidadeList(GroupRequiredMixin, LoginRequiredMixin, GrupoMixin, ListView):
    login_url = reverse_lazy('login')
    group_required = u'Administrador'
    model = Especialidade
    template_name = 'cadastros/listas/especialidade.html'
    success_url = reverse_lazy('listar-especialidades')


class MedicoList(LoginRequiredMixin, GrupoMixin, ListView):
    login_url = reverse_lazy('login')
    model = Medico
    template_name = 'cadastros/listas/medico.html'
    success_url = reverse_lazy('listar-medicos')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titulo'] = 'Médicos'
        return context


class PacienteList(LoginRequiredMixin, GrupoMixin, ListView):
    login_url = reverse_lazy('login')
    model = Paciente
    template_name = 'cadastros/listas/paciente.html'
    success_url = reverse_lazy('listar-pacientes')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titulo'] = 'Pacientes'
        return context


class ProcedimentoList(LoginRequiredMixin, GrupoMixin, ListView):
    login_url = reverse_lazy('login')
    model = Procedimento
    template_name = 'cadastros/listas/procedimento.html'
    success_url = reverse_lazy('listar-procedimentos')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titulo'] = 'Procedimento'
        return context

# --------------- Views para Detalhar dados ---------------
class FuncionarioDetail(GroupRequiredMixin, LoginRequiredMixin, GrupoMixin, DetailView):
    login_url = reverse_lazy('login')
    group_required = u'Administrador'
    model = Funcionario
    template_name = 'cadastros/listas/dados_funcionario.html'
    context_object_name = 'funcionario'


class MedicoDetail(GroupRequiredMixin, LoginRequiredMixin, GrupoMixin, DetailView):
    login_url = reverse_lazy('login')
    group_required = u'Administrador'
    model = Medico
    template_name = 'cadastros/listas/dados_medico.html'
    context_object_name = 'medico'


class PacienteDetail(GroupRequiredMixin, LoginRequiredMixin, GrupoMixin, DetailView):
    login_url = reverse_lazy('login')
    group_required = u'Administrador'
    model = Paciente
    template_name = 'cadastros/listas/dados_paciente.html'
    context_object_name = 'paciente'


class AgendaDetail(GroupRequiredMixin, LoginRequiredMixin, GrupoMixin, DetailView):
    login_url = reverse_lazy('login')
    group_required = u'Administrador'
    model = AgendaMedico
    template_name = 'cadastros/agenda.html'
    context_object_name = 'agenda'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        agenda = AgendaMedico.objects.get(pk=pk)
        horarios_ordenados = HorarioMedico.objects.filter(agenda=agenda).order_by('dia_semana')
        dia_semana_nomes = dict(dias_semana_opcoes)

        for horario in horarios_ordenados:
            horario.dia_semana = dia_semana_nomes.get(horario.dia_semana, '').split('-')[0]
        
        context['horarios'] = horarios_ordenados
        return context


# --------------- Todas as Views de Horário ---------------
class HorarioCreate(GroupRequiredMixin, LoginRequiredMixin, GrupoMixin, CreateView):
    login_url = reverse_lazy('login')
    group_required = u'Administrador'
    model = HorarioMedico
    form_class = HorarioMedicoForm
    template_name = 'cadastros/modal_agenda.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        agenda = AgendaMedico.objects.get(pk=pk)
        horarios_ordenados = HorarioMedico.objects.filter(agenda=agenda).order_by('dia_semana')
        dia_semana_nomes = dict(dias_semana_opcoes)

        for horario in horarios_ordenados:
            horario.dia_semana = dia_semana_nomes.get(horario.dia_semana, '').split('-')[0]
        
        context['titulo'] = 'Adicionar Novo Horário'
        context['btn_texto'] = 'Salvar'
        context['horarios'] = horarios_ordenados
        context['agenda'] = agenda
        return context

    def get_success_url(self):
        return reverse('dados-agenda', args=[str(self.object.agenda.id)])


class HorarioUpdate(GroupRequiredMixin, LoginRequiredMixin, GrupoMixin, UpdateView):
    login_url = reverse_lazy('login')
    group_required = u'Administrador'
    model = HorarioMedico
    form_class = HorarioMedicoForm
    template_name = 'cadastros/modal_agenda.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fk = self.kwargs.get('fk')
        agenda = AgendaMedico.objects.get(pk=fk)
        horarios_ordenados = HorarioMedico.objects.filter(agenda=agenda).order_by('dia_semana')
        dia_semana_nomes = dict(dias_semana_opcoes)

        for horario in horarios_ordenados:
            horario.dia_semana = dia_semana_nomes.get(horario.dia_semana, '').split('-')[0]
        
        context['titulo'] = 'Editar Horário'
        context['btn_texto'] = 'Salvar'
        context['horarios'] = horarios_ordenados
        context['agenda'] = agenda
        return context

    def get_success_url(self):
        return reverse('dados-agenda', args=[str(self.object.agenda.id)])


class HorarioDelete(GroupRequiredMixin, LoginRequiredMixin, GrupoMixin, DeleteView):
    login_url = reverse_lazy('login')
    group_required = u'Administrador'
    model = HorarioMedico
    template_name = 'cadastros/modal_excluir.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fk = self.kwargs.get('fk')
        agenda = AgendaMedico.objects.get(pk=fk)
        horarios_ordenados = HorarioMedico.objects.filter(agenda=agenda).order_by('dia_semana')
        dia_semana_nomes = dict(dias_semana_opcoes)

        for horario in horarios_ordenados:
            horario.dia_semana = dia_semana_nomes.get(horario.dia_semana, '').split('-')[0]
        
        context['titulo'] = 'Excluir Horário'
        context['btn_texto'] = 'Confirmar'
        context['horarios'] = horarios_ordenados
        context['agenda'] = agenda
        return context

    def get_success_url(self):
        return reverse('dados-agenda', args=[str(self.object.agenda.id)])


