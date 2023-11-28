from django.urls import path

#from relatorios.views import GerarFichaPaciente
from .views import Agendamentos_PDF, AniversariosPacientes_PDF, GerarFichaFuncionario, GerarFichaFuncionarioPDF, GerarFichaPaciente, GerarFichaPacientePDF, GerarReciboPDF, ProntuarioPDF, RelatorioFinanceiroPDF

urlpatterns = [
    path('ficha/paciente/<int:pk>/pdf/', GerarFichaPacientePDF.as_view(), name='ficha-paciente-pdf'),
    path('ficha/pacientehtml/<int:pk>', GerarFichaPaciente.as_view(), name='ficha-paciente'),
    path('ficha/funcionario/<int:pk>/pdf/', GerarFichaFuncionarioPDF.as_view(), name='ficha-funcionario-pdf'),
    path('ficha/funcionariohtml/<int:pk>', GerarFichaFuncionario.as_view(), name='ficha-funcionario'),
    path('aniversarios/pacientes/pdf/', AniversariosPacientes_PDF.as_view(), name='aniversarios-pacientes-pdf'),
    path('agendamentos/pdf/', Agendamentos_PDF.as_view(), name='agendamentos-pdf'),
    path('relatorio/financeiro/pdf/', RelatorioFinanceiroPDF.as_view(), name='relatorio-financeiro-pdf'),
    path('gerar/recibo/pdf/<int:pk>', GerarReciboPDF.as_view(), name='gerar-recibo-pdf'),
    path('gerar/prontuario/pdf/<int:pk>', ProntuarioPDF.as_view(), name='gerar-prontuario-pdf'),
]