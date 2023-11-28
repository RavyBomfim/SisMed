from django.urls import path
from .views import AgendamentoCreate, AgendamentoDelete, AgendamentoList, AgendamentoUpdate, AgendamentosComMedico, AtendimentoCreate, Detalhes_Agendamento, MostrarProntuario, PacientesDoDia, PacientesDoDiaMedico, ProntuarioList, RelatorioFinanceiro, IndexView, concluir_procedimento, medicos_procedimento, retornar_horarios, valor_consulta

urlpatterns = [
    #urls visualização
    path('inicio', IndexView.as_view(), name='inicio'),
    path('relatorio/financeiro', RelatorioFinanceiro.as_view(), name='relatorio-financeiro'),

    #urls cadastros
    path('agendar/consulta/procedimento', AgendamentoCreate.as_view(),  name='agendar-consulta-procedimento'),
    path('registrar/atendimento/consulta<int:pk>', AtendimentoCreate.as_view(), name='registrar-atendimento'),
    

    #urls pada edição
    path('editar/agendamento/<int:pk>', AgendamentoUpdate.as_view(), name='editar-agendamento'),
    path('concluir/procedimento', concluir_procedimento, name='concluir-procedimento'),

    #urls para deletar
    path('excluir/agendamento/<int:pk>', AgendamentoDelete.as_view(), name='excluir-agendamento'),

    #urls para listagem
    path('listar/agendamentos', AgendamentoList.as_view(), name='listar-agendamentos'),
    path('listar/agendamentos/medico', AgendamentosComMedico.as_view(), name='agendamentos-com-medico'),
    path('pacientes/dia', PacientesDoDia.as_view(), name='pacientes-do-dia'),
    path('pacientes/dia/medico', PacientesDoDiaMedico.as_view(), name='pacientes-do-dia-medico'),
    path('listar/prontuarios', ProntuarioList.as_view(), name='listar-prontuarios'),

    #urls para detalhar
    path('detalhes/agendamento/<int:pk>', Detalhes_Agendamento.as_view(), name='detalhes_agendamento'),
    path('dados/prontuario/<int:pk>', MostrarProntuario.as_view(), name='dados_prontuario'),

    # Urls para requisições json
    path('medico_responsavel/<int:procedimento_id>/', medicos_procedimento, name='medicos_procedimento'),
    path('retornar-horarios', retornar_horarios, name='retornar-horarios'),
    path('valor-consulta', valor_consulta, name='valor-consulta'),
]