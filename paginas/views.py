from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import GroupRequiredMixin
from cadastros.models import AgendamentoConsulta, Especialidade, Medico, Paciente
from django.db.models import Count
from datetime import date

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
        context['qtd_consultas'] = AgendamentoConsulta.objects.filter(data_hora__date=data_atual).count()
        context['especialidades_mais_requisitadas'] = Especialidade.objects.annotate(num_consultas=Count('medico__agendamentoconsulta')).order_by('-num_consultas')[:3]
        return context