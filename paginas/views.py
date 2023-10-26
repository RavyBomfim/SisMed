import json
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import GroupRequiredMixin
from cadastros.models import AgendaMedico, AgendamentoConsulta, Especialidade, HorarioAtendimento, HorarioMedico, Medico, Paciente
from django.db.models import Count
from datetime import date, datetime, time
from paginas.forms import AgendamentoConsultaForm

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


class IndexView(LoginRequiredMixin, GrupoMixin, TemplateView):
    login_url = reverse_lazy('login')
    template_name = "paginas/index.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['qtd_medicos'] = Medico.objects.all().count()
        context['qtd_pacientes'] = Paciente.objects.all().count()
        data_atual = date.today()
        context['data_atual'] = data_atual
        context['qtd_consultas'] = AgendamentoConsulta.objects.filter(data=data_atual).count()
        context['especialidades_mais_requisitadas'] = Especialidade.objects.annotate(num_consultas=Count('medico__agendamentoconsulta')).order_by('-num_consultas')[:3]
        return context
    

class Teste(LoginRequiredMixin, GrupoMixin, TemplateView):
    login_url = reverse_lazy('login')
    template_name = "paginas/teste-form.html"


class AgendarConsulta(LoginRequiredMixin, GrupoMixin, CreateView):
    login_url = reverse_lazy('login')
    model = AgendamentoConsulta
    form_class = AgendamentoConsultaForm
    template_name = 'paginas/agendamento_consultas.html'
    success_url = reverse_lazy('consultas-agendadas')


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


def get_horarios_disponiveis(medico_id, data, agendados=False):
    # Obtenha os horários de atendimento da model HorarioAtendimento
    horarios_atendimento = HorarioAtendimento.objects.all().values_list('horario_atendimento', flat=True)

    # Mapeamento dos números para os nomes dos dias da semana
    dia_semana_opcoes = {0: 'Segunda-feira', 1: 'Terça-feira', 2: 'Quarta-feira', 3: 'Quinta-feira', 4: 'Sexta-feira', 5: 'Sábado'}

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
    horarios_agend = AgendamentoConsulta.objects.filter(
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


class HorariosDisponiveis(LoginRequiredMixin, GrupoMixin, TemplateView):
    login_url = reverse_lazy('login')
    template_name = 'paginas/horarios.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        medico_id = 4
        data = '2023-10-24'

        horarios = get_horarios_disponiveis(medico_id, data, True)

        horarios_disponiveis = horarios[0]
        horarios_agendados = horarios[1]
        horarios_disponiveis_manha = horarios[2]
        horarios_disponiveis_tarde = horarios[3]

        context['horarios_disponiveis_manha'] = horarios_disponiveis_manha
        context['horarios_disponiveis_tarde'] = horarios_disponiveis_tarde
        context['horarios_disponiveis'] = horarios_disponiveis
        context['horarios_agendados'] = horarios_agendados

        return context 



class VerAgendas(LoginRequiredMixin, GrupoMixin, TemplateView):
    login_url = reverse_lazy('login')
    template_name = 'paginas/agendas.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Obtenha os horários de atendimento da model HorarioAtendimento
        horarios_atendimento = HorarioAtendimento.objects.all().values_list('horario_atendimento', flat=True)

        # Mapeamento dos números para os nomes dos dias da semana
        dia_semana_opcoes = {0: 'Segunda-feira', 1: 'Terça-feira', 2: 'Quarta-feira', 3: 'Quinta-feira', 4: 'Sexta-feira', 5: 'Sábado'}

        # Dicionário para armazenar horários disponíveis por médico e dia da semana
        horarios_por_medico = {}

        for dia in range(6):  # 0 a 5 representa de segunda a sábado
            horarios_medico_manha = HorarioMedico.objects.filter(
                dia_semana=dia,
                horario_inicial_manha__isnull=False,
            )

            horarios_medico_tarde = HorarioMedico.objects.filter(
                dia_semana=dia,
                horario_inicial_tarde__isnull=False,
            )

            for horario_medico in horarios_medico_manha:
                medico = horario_medico.agenda.medico
                inicio_manha = horario_medico.horario_inicial_manha
                final_manha = horario_medico.horario_final_manha
                chave = (medico.nome_completo, dia_semana_opcoes[dia])

                if chave not in horarios_por_medico:
                    horarios_por_medico[chave] = []

                for horario in horarios_atendimento:
                    if inicio_manha <= horario < final_manha:
                        horarios_por_medico[chave].append(horario.strftime("%H:%M"))

            for horario_medico in horarios_medico_tarde:
                medico = horario_medico.agenda.medico
                inicio_tarde = horario_medico.horario_inicial_tarde
                final_tarde = horario_medico.horario_final_tarde
                chave = (medico.nome_completo, dia_semana_opcoes[dia])

                if chave not in horarios_por_medico:
                    horarios_por_medico[chave] = []

                for horario in horarios_atendimento:
                    if inicio_tarde <= horario < final_tarde:
                        horarios_por_medico[chave].append(horario.strftime("%H:%M"))

        context['horarios_disponiveis'] = horarios_por_medico
        return context

# --------------- Views para Listar ---------------
class AgendConsultaList(LoginRequiredMixin, GrupoMixin, ListView):
    login_url = reverse_lazy('login')
    model = AgendamentoConsulta
    template_name = 'paginas/listas/consultas_agendadas.html'