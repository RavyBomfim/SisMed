import json
from django.http import JsonResponse
from django.db.models import Sum
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from cadastros.models import AgendaMedico, Agendamento, Atendimento, Especialidade, HorarioAtendimento, HorarioMedico, Medico, Paciente, Procedimento, Prontuario
from django.db.models import Count
from datetime import date, datetime
from paginas.forms import AgendamentoForm, AtendimentoForm
from django.utils import timezone
from django.contrib.auth.decorators import user_passes_test

# Create your views here.
class GrupoMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        is_admin = user.groups.filter(name='Administrador').exists()
        is_medico = user.groups.filter(name='Medico').exists()
        context['is_admin'] = is_admin
        context['is_medico'] = is_medico
        return context


def is_medico(user):
    return user.groups.filter(name='Medico').exists()


def medicos_procedimento(request, procedimento_id):
    try:
        procedimento = Procedimento.objects.get(pk=procedimento_id)
        especialidade = procedimento.especialidade_responsavel
        medicos = Medico.objects.filter(especialidade=especialidade)
        medicos_data = [{'id': medico.id, 'nome_completo': medico.nome_completo, 'especialidade': medico.especialidade.especialidade} for medico in medicos]
        return JsonResponse({'medicos': medicos_data, 'valor_procedimento': procedimento.valor_procedimento})
    except Procedimento.DoesNotExist:
        return JsonResponse({'error': 'Procedimento não encontrado'}, status=404)


# -------- Funçao que retorna o valor da consulta com base na especialidade do médico --------
def valor_consulta(request):
    if request.method == 'POST':
        try:
            dados = json.loads(request.body.decode('utf-8'))
            medico_id = dados.get('medico_id')
            valor_consulta = 0.00

            if medico_id:
                try:
                    medico = Medico.objects.get(id=medico_id)
                    valor_consulta = medico.especialidade.valor_consulta if medico.especialidade else 0.00
                except Medico.DoesNotExist:
                    pass

            return JsonResponse({'valor_consulta': valor_consulta})
        except json.JSONDecodeError:
            return JsonResponse({'erro': 'Falha ao decodificar os dados JSON'}, status=400)
    else:
        return JsonResponse({'erro': 'Apenas métodos POST são permitidos'})
      

# -------- Funçao que retorna aviso sobre os dias que um determi nado médico atende --------
def retornar_aviso(arg):
    aviso = ''
    for indice, dia in enumerate(arg):
        if indice == 0:
            if len(arg) == 1:
                aviso += dia + '.'
            else: 
                aviso += dia.split('-')[0]
        elif indice != len(arg) - 1:
            aviso += ', ' + dia.split('-')[0]
        else:
            aviso += ' e ' + dia + '.' 
    return aviso   


# -------- Funçao que retorna os horários disponíveis do médico em uma determinada data --------
def get_horarios_disponiveis(medico_id, data, agendados=False):
    # Obtenha os horários de atendimento da model HorarioAtendimento
    horarios_atendimento = HorarioAtendimento.objects.all().values_list('horario_atendimento', flat=True)

    # Convertendo a data fornecida em um objeto de data
    data_obj = datetime.strptime(data, '%Y-%m-%d')
    dia_semana = data_obj.weekday()  # Obtém o número do dia da semana (0 a 6, onde 0 é segunda-feira)

    horarios_disponiveis_manha = []
    horarios_disponiveis_tarde = []

    # Obtendo os registros da model HorarioMedico para o médico específico e o dia da semana correspondente
    horarios_medico_manha = HorarioMedico.objects.filter(
        dia_semana=dia_semana,
        horario_inicial_manha__isnull=False,
        agenda__medico__id=medico_id,
    )

    horarios_medico_tarde = HorarioMedico.objects.filter(
        dia_semana=dia_semana,
        horario_inicial_tarde__isnull=False,
        agenda__medico__id=medico_id,
    )

    # Criando uma lista de horários já agendados para o médico e data especificados
    horarios_agend = Agendamento.objects.filter(
        medico__id=medico_id,
        data=data,
        horario__in=horarios_atendimento  # Filtrando por horários de atendimento
    ).values_list('horario', flat=True)

    for horario_medico in horarios_medico_manha:
        inicio_manha = horario_medico.horario_inicial_manha
        final_manha = horario_medico.horario_final_manha

        for horario in horarios_atendimento:
            if inicio_manha <= horario < final_manha:
                horarios_disponiveis_manha.append(horario.strftime("%H:%M"))

    for horario_medico in horarios_medico_tarde:
        inicio_tarde = horario_medico.horario_inicial_tarde
        final_tarde = horario_medico.horario_final_tarde

        for horario in horarios_atendimento:
            if inicio_tarde <= horario < final_tarde:
                horarios_disponiveis_tarde.append(horario.strftime("%H:%M"))

    horarios_agendados = []
    for horario in horarios_agend:
        horarios_agendados.append(horario.strftime("%H:%M"))

    horarios_disponiveis = sorted(horarios_disponiveis_manha) + sorted(horarios_disponiveis_tarde)
    for horario in horarios_disponiveis:
        if horario in horarios_agendados:
            horarios_disponiveis.remove(horario)

    aviso = ''

    if len(horarios_disponiveis_manha) == 0 and len(horarios_disponiveis_tarde) == 0:
        medico = Medico.objects.get(id=medico_id)
        agenda_medico = AgendaMedico.objects.get(medico=medico)
        dias_atend = HorarioMedico.objects.filter(agenda=agenda_medico).order_by('dia_semana')
          
        dias_atendimento = []
        for dia in dias_atend:
            dias_atendimento.append(dia.get_dia_semana_display())

        sexo = medico.sexo
        if sexo == 'F':
            aviso = 'A médica requisitada atende apenas nos dias de '
            aviso += retornar_aviso(dias_atendimento)
        else:
            aviso = 'O médico requisitado atende apenas nos dias de '
            aviso += retornar_aviso(dias_atendimento)

    if len(horarios_disponiveis) == 0 and (len(horarios_disponiveis_manha) > 0 or len(horarios_disponiveis_manha) > 0):
        aviso = 'Todos os horários deste médico para este dia já foram agendados'

    if agendados: 
        return horarios_disponiveis, horarios_agendados, horarios_disponiveis_manha, horarios_disponiveis_tarde
    else:
        return horarios_disponiveis, aviso


# -------- Funçao que recebe o id do médico e a data e retorna os horários disponíveis para a requisição json --------
def retornar_horarios(request):
    if request.method == 'POST':
        try:
            dados = json.loads(request.body.decode('utf-8'))
            medico_id = dados.get('medico_id')
            data = dados.get('data_agend')

            dados = get_horarios_disponiveis(medico_id, data)

            horarios_disponiveis = dados[0]
            aviso = dados[1]

            data_response = {'horarios_disponiveis': horarios_disponiveis, 'aviso': aviso}
            return JsonResponse(data_response)
        except json.JSONDecodeError:
            return JsonResponse({'erro': 'Falha ao decodificar os dados JSON'}, status=400)
    else:
        return JsonResponse({'erro': 'Apenas métodos POST são permitidos'})


# --------------- TemplateViews ---------------

class IndexView(LoginRequiredMixin, GrupoMixin, TemplateView):
    login_url = reverse_lazy('login')
    template_name = "paginas/index.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        if self.request.user.groups.filter(name='Medico').exists():
            medico_do_usuario = Medico.objects.get(usuario=self.request.user)
            qtd_pacientes = Paciente.objects.filter(agendamento__medico=medico_do_usuario).distinct().count()
            card_pacientes = 'Meus Pacientes'
        else:
            qtd_pacientes = Paciente.objects.all().count()
            card_pacientes = 'Pacientes Cadastrados'

        context['qtd_medicos'] = Medico.objects.all().count()
        context['titulo_card_pacientes'] = card_pacientes
        context['qtd_pacientes'] = qtd_pacientes
        data_atual = date.today()
        context['data_atual'] = data_atual
        context['qtd_consultas'] = Agendamento.objects.filter(data=data_atual).count()
        context['especialidades_mais_requisitadas'] = Especialidade.objects.annotate(num_consultas=Count('medico__agendamento')).order_by('-num_consultas')[:3]
        return context

# --------------- Views de Cadastro ---------------

class AgendamentoCreate(LoginRequiredMixin, GrupoMixin, CreateView):
    login_url = reverse_lazy('login')
    group_required = u'Administrador'
    model = Agendamento
    form_class = AgendamentoForm
    template_name = 'paginas/form_agendamento.html'
    success_url = reverse_lazy('listar-agendamentos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type_view'] = 'CreateView'
        return context
    

# --------------- Views para Edição ---------------

class AgendamentoUpdate(LoginRequiredMixin, GrupoMixin, UpdateView):
    login_url = reverse_lazy('login')
    group_required = u'Administrador'
    model = Agendamento
    form_class = AgendamentoForm
    template_name = 'paginas/form_agendamento.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        agendamento = Agendamento.objects.get(pk=pk)

        procedimento = ''
        if agendamento.tipo_agendamento == 'Procedimento':
            procedimento_nome = agendamento.procedimento
            if (procedimento_nome):
                procedimento = get_object_or_404(Procedimento, nome_procedimento=procedimento_nome)
                context['procedimento_id'] = procedimento.id

        data = agendamento.data.strftime('%Y-%m-%d')
        context['data'] = data
        context['horario'] = agendamento.horario
        context['type_view'] = 'UpdateView'
        return context

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        agendamento = Agendamento.objects.get(pk=pk)
        
        if agendamento.concluido:
            messages.error(request, 'Não é possível editar consulta/procedimento concluído.')
            return redirect('detalhes_agendamento', pk=agendamento.id)
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        pk = self.kwargs.get('pk')
        return reverse('detalhes_agendamento', kwargs={'pk': pk})

# --------------- Views para excluir  ---------------

class AgendamentoDelete(LoginRequiredMixin, GrupoMixin, DeleteView):
    login_url = reverse_lazy('login')
    group_required = u'Administrador'
    model = Agendamento
    template_name = 'cadastros/form_excluir.html'
    success_url = reverse_lazy('listar-agendamentos')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['objeto'] = 'esse registro de agendamento'
        return context

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        agendamento = Agendamento.objects.get(pk=pk)

        if agendamento.concluido:
            messages.error(request, 'Não é possível excluir consulta/procedimento concluído.')
            return redirect('detalhes_agendamento', pk=agendamento.id)
        return super().get(request, *args, **kwargs)


# --------------- Views para Listar ---------------

class AgendamentoList(LoginRequiredMixin, GrupoMixin, ListView):
    login_url = reverse_lazy('login')
    model = Agendamento
    template_name = 'paginas/listas/agendamentos.html'

    def get_queryset(self):
        data_agend = self.request.GET.get('data-pesquisada')
        especialidade_agend = self.request.GET.get('especialidade-pesquisada')

        agendamentos = Agendamento.objects.all()
        
        if data_agend and especialidade_agend:
            agendamentos = agendamentos.filter(data=data_agend, medico__especialidade__especialidade=especialidade_agend)
        elif data_agend:
            agendamentos = agendamentos.filter(data=data_agend)
        elif especialidade_agend:
            agendamentos = agendamentos.filter(medico__especialidade__especialidade=especialidade_agend)

        return agendamentos
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        titulo = 'Agendamentos'
        aviso = 'Ainda não há nenhum registro de agendamento de consultas ou procedimentos'
        data_agend = self.request.GET.get('data-pesquisada')
        especialidade_agend = self.request.GET.get('especialidade-pesquisada')

        if data_agend and data_agend != '' and data_agend != 'None' and especialidade_agend and especialidade_agend != '' and especialidade_agend != 'None':
            data = datetime.strptime(data_agend, '%Y-%m-%d').strftime('%d/%m/%Y')
            titulo = f'Agendamentos do dia {data} para {especialidade_agend}s'
            aviso = 'Não há consultas ou procedimentos registrados para esta data e especialidade'
        elif especialidade_agend and especialidade_agend != '' and especialidade_agend != 'None':
            titulo = f'Agendamentos para {especialidade_agend}s'
            aviso = 'Não há consultas ou procedimentos registrados para esta especialidade'
        elif data_agend and data_agend != '' and data_agend != 'None':
            data = datetime.strptime(data_agend, '%Y-%m-%d').strftime('%d/%m/%Y')
            titulo = f'Agendamentos do dia {data}'
            aviso = 'Não há consultas ou procedimentos registrados para esta data'

        context['especialidades'] = Especialidade.objects.all()
        context['titulo'] = titulo
        context['aviso'] = aviso
        context['data'] = data_agend
        context['especialidade_pesq'] = especialidade_agend
        return context


class AgendamentosComMedico(AgendamentoList):
    group_required = u'Medico'

    def get_queryset(self):
        data_agend = self.request.GET.get('data-pesquisada')
        
        if data_agend:
            agendamentos = Agendamento.objects.filter(
                data=data_agend,
                medico__usuario=self.request.user
            )
        else: 
            agendamentos = Agendamento.objects.filter(medico__usuario=self.request.user)

        return agendamentos


class PacientesDoDia(LoginRequiredMixin, GrupoMixin, ListView):
    login_url = reverse_lazy('login')
    model = Agendamento
    template_name = 'paginas/listas/pacientes_do_dia.html'
    data_atual = date.today()

    def get_queryset(self):
        return Agendamento.objects.filter(data=self.data_atual)
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titulo'] = 'Pacientes do dia'
        context['data_atual'] = self.data_atual
        return context


class PacientesDoDiaMedico(PacientesDoDia):
    group_required = u'Medico'

    def get_queryset(self):
        return Agendamento.objects.filter(data=self.data_atual, medico__usuario=self.request.user)
    

# --------------- Views para Detalhar ---------------
class Detalhes_Agendamento(LoginRequiredMixin, GrupoMixin, DetailView):
    login_url = reverse_lazy('login')
    model = Agendamento
    template_name = 'paginas/listas/detalhes_agendamento.html'


def calcular_idade(data_nascimento):
    hoje = timezone.now().date()
    idade = hoje.year - data_nascimento.year - ((hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day))
    return idade


class MostrarProntuario(LoginRequiredMixin, GrupoMixin, DetailView):
    group_required = u'[Administrador, Medico]'
    login_url = reverse_lazy('login')
    model = Prontuario
    template_name = 'paginas/prontuario.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        pk = self.kwargs.get('pk')
        prontuario = Prontuario.objects.get(pk=pk)
        paciente = prontuario.paciente
        data_nascimento = paciente.data_nascimento
        idade_paciente = calcular_idade(data_nascimento)

        consultas = Agendamento.objects.filter(paciente=paciente.id, tipo_agendamento = 'Consulta', 
        concluido=True)
        procedimentos = Agendamento.objects.filter(paciente=paciente.id, tipo_agendamento = 'Procedimento', concluido=True)

        print(idade_paciente)
        context['paciente_idade'] = idade_paciente
        context['paciente'] = paciente
        context['titulo'] = 'Prontuário'
        context['consultas'] = consultas
        context['procedimentos'] = procedimentos
        return context
    

class AtendimentoCreate(LoginRequiredMixin, GrupoMixin, CreateView):
    login_url = reverse_lazy('login')
    group_required = u'Medico'
    model = Atendimento
    form_class = AtendimentoForm
    template_name = 'paginas/modal_atendimento.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        agendamento = Agendamento.objects.get(pk=pk)
        context['agendamento'] = agendamento
        context['titulo'] = 'Informações de Atendimento'
        return context
    
    def get_success_url(self):
        pk = self.kwargs.get('pk')
        agendamento = Agendamento.objects.get(pk=pk)
        agendamento.concluido = True
        agendamento.save()
        return reverse('detalhes_agendamento', kwargs={'pk': pk})
    
@user_passes_test(is_medico)
def concluir_procedimento(request):
    if request.method == 'POST':
        agendamento_id = request.POST.get('agendamento_id')
        agendamento = get_object_or_404(Agendamento, pk=agendamento_id)
        # Marcar procedimento como concluído
        agendamento.concluido = True
        agendamento.save()
        return redirect('detalhes_agendamento', pk=agendamento.id)


class RelatorioFinanceiro(LoginRequiredMixin, GrupoMixin, TemplateView):
    login_url = reverse_lazy('login')
    group_required = u'Administrador'
    template_name = "paginas/relatorio_financeiro.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        valor_total = Agendamento.objects.filter(concluido=True).aggregate(Sum('valor'))['valor__sum']

        titulo ='Relatório Financeiro Geral'

        especialidades = Especialidade.objects.all()
        lista_consultas_por_especialidade = []

        periodo_inicial = self.request.GET.get('periodo-inicial')
        periodo_final = self.request.GET.get('periodo-final')

        if periodo_inicial and periodo_final and periodo_inicial != '' and periodo_final != '' and periodo_inicial != 'None' and periodo_final != 'None':
            valor_total = Agendamento.objects.filter(concluido=True,
                data__range=[periodo_inicial, periodo_final]).aggregate(Sum('valor'))['valor__sum']
            
            data_inicial = datetime.strptime(periodo_inicial, '%Y-%m-%d').strftime('%d/%m/%Y')
            data_final = datetime.strptime(periodo_final, '%Y-%m-%d').strftime('%d/%m/%Y')
            titulo = f'Relatório Financeiro de {data_inicial} a {data_final}'

        especialidades = Especialidade.objects.all()

        lista_consultas_por_especialidade = []

        for especialidade in especialidades:

            if periodo_inicial and periodo_final and periodo_inicial != '' and periodo_final != '' and periodo_inicial != 'None' and periodo_final != 'None':
                total_consultas = Agendamento.objects.filter(
                    medico__especialidade=especialidade,
                    concluido=True,
                    data__range=[periodo_inicial, periodo_final]
                ).count()

                valor_arrecadado = Agendamento.objects.filter(
                    medico__especialidade=especialidade,
                    concluido=True,
                    data__range=[periodo_inicial, periodo_final]
                ).aggregate(Sum('valor'))['valor__sum'] or 0

                total_retornos = Agendamento.objects.filter(
                    medico__especialidade=especialidade,
                    retorno=True,
                    concluido=True,
                    data__range=[periodo_inicial, periodo_final]
                ).count()
            else:
                total_consultas = Agendamento.objects.filter(medico__especialidade=especialidade, concluido=True).count()
                valor_arrecadado = Agendamento.objects.filter(medico__especialidade=especialidade, concluido=True).aggregate(Sum('valor'))['valor__sum'] or 0
                total_retornos = Agendamento.objects.filter(medico__especialidade=especialidade, retorno=True, concluido=True).count()

            lista_consultas_por_especialidade.append({
                'especialidade': especialidade.especialidade, 
                'total_consultas': total_consultas, 
                'valor_arrecadado': valor_arrecadado,
                'total_retornos': total_retornos
            })

        lista_consultas_por_especialidade = sorted(lista_consultas_por_especialidade, key=lambda x: x['valor_arrecadado'], reverse=True)
        context['titulo'] = titulo
        context['consultas_por_especialidade'] = lista_consultas_por_especialidade
        context['total_valor'] = valor_total
        context['data_inicial'] = periodo_inicial
        context['data_final'] = periodo_final

        return context