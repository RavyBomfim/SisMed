from django.urls import path
from .views import AgendConsultaList, AgendarConsulta, HorariosDisponiveis, Teste, IndexView, VerAgendas, retornar_horarios, valor_consulta

urlpatterns = [
    path('inicio', IndexView.as_view(), name='inicio'),
    path('agendar/consulta', AgendarConsulta.as_view(), name='agendar-consulta'),
    path('horarios-disponiveis', HorariosDisponiveis.as_view(), name='horarios-disponiveis'),
    path('retornar-horarios', retornar_horarios, name='retornar-horarios'),
    path('valor-consulta', valor_consulta, name='valor-consulta'),
    path('ver-agendas', VerAgendas.as_view(), name='ver-agendas'),
    path('consultas/agendadas', AgendConsultaList.as_view(), name='consultas-agendadas'),
    path('teste', Teste.as_view(), name='teste'),
]