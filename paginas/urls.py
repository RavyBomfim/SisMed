from django.urls import path
from .views import AgendamentoDelete, AgendamentoList, AgendamentoUpdate, AgendarConsulta, Detalhes_Agendamento, PacientesDoDia, Teste, IndexView, medicos_procedimento, retornar_horarios, valor_consulta

urlpatterns = [
    #urls visualização
    path('inicio', IndexView.as_view(), name='inicio'),
    path('teste', Teste.as_view(), name='teste'),

    #urls cadastros
    path('agendar/consulta', AgendarConsulta.as_view(), name='agendar-consulta'),

    #urls pada edição
    path('editar/agendamento/<int:pk>', AgendamentoUpdate.as_view(), name='editar-agendamento'),

    #urls para deletar
    path('deletar/agendamento/<int:pk>', AgendamentoDelete.as_view(), name='excluir-agendamento'),

    #urls para listagem
    path('agendamentos', AgendamentoList.as_view(), name='agendamentos'),
    path('pacientes-do-dia', PacientesDoDia.as_view(), name='pacientes-do-dia'),

    #urls para detalhar
    path('detalhes_agendamento/<int:pk>', Detalhes_Agendamento.as_view(), name='detalhes_agendamento'),

    # Urls para requisições json
    path('medico_responsavel/<int:procedimento_id>/', medicos_procedimento, name='medicos_procedimento'),
    path('retornar-horarios', retornar_horarios, name='retornar-horarios'),
    path('valor-consulta', valor_consulta, name='valor-consulta'),
]