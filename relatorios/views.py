from datetime import datetime
from django.db.models import F, ExpressionWrapper, IntegerField
from django.db.models.functions import ExtractDay, ExtractMonth
from utils.config import get_wkhtmltopdf_path
from django.urls import reverse_lazy
#from .utils import GeradorDePDF
from cadastros.models import Agendamento, Funcionario, Paciente, Prontuario
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import GroupRequiredMixin
from paginas.views import AgendamentoList, GrupoMixin, MostrarProntuario, RelatorioFinanceiro
from django.http import HttpResponse
from django.template.loader import get_template
import pdfkit
from urllib.parse import quote
import logging
from cadastros.utils import nome_mes

logger = logging.getLogger(__name__)

class GerarFichaPacientePDF(GroupRequiredMixin, LoginRequiredMixin, GrupoMixin, DetailView):
    login_url = reverse_lazy('login')
    group_required = u'Administrador'
    model = Paciente
    template_name = 'relatorios/ficha_paciente.html'

    def get(self, request, *args, **kwargs):
        paciente = self.get_object()
        template = get_template(self.template_name)
        context = {'paciente': paciente}
        html_content = template.render(context)

        # Caminho para o executável wkhtmltopdf
        wkhtmltopdf_path = get_wkhtmltopdf_path()

        url = 'http://127.0.0.1:8000/' + quote(f'ficha/paciente/{paciente.pk}/pdf/')

        pdfkit_config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)

        try:
            pdf_file = pdfkit.from_string(html_content, False, configuration=pdfkit_config)
            response = HttpResponse(pdf_file, content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename="Ficha do Paciente - {}.pdf"'.format(paciente.nome_completo)

            return response
        except Exception as e:
            logger.error(f"Erro ao gerar PDF: {e}")
            return HttpResponse(f"Erro ao gerar PDF: {e}", status=500)
        

class GerarFichaFuncionarioPDF(GroupRequiredMixin, LoginRequiredMixin, GrupoMixin, DetailView):
    login_url = reverse_lazy('login')
    group_required = u'Administrador'
    model = Funcionario
    template_name = 'relatorios/ficha_funcionario.html'

    def get(self, request, *args, **kwargs):
        funcionario = self.get_object()
        template = get_template(self.template_name)
        context = {'funcionario': funcionario}
        html_content = template.render(context)

        # Caminho para o executável wkhtmltopdf
        wkhtmltopdf_path = get_wkhtmltopdf_path()
        pdfkit_config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)

        try:
            pdf_file = pdfkit.from_string(html_content, False, configuration=pdfkit_config)
            response = HttpResponse(pdf_file, content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename="Ficha do Funcionário - {}.pdf"'.format(funcionario.nome_completo)

            return response
        except Exception as e:
            logger.error(f"Erro ao gerar PDF: {e}")
            return HttpResponse(f"Erro ao gerar PDF: {e}", status=500)


class AniversariosPacientes_PDF(LoginRequiredMixin, GrupoMixin, ListView):
    login_url = reverse_lazy('login')
    model = Paciente
    ordering = ['data_nascimento']
    template_name = 'relatorios/aniversarios_pdf.html'

    def get_queryset(self):
        day_expr = ExpressionWrapper(ExtractDay('data_nascimento'), output_field=IntegerField())
        month_expr = ExpressionWrapper(ExtractMonth('data_nascimento'), output_field=IntegerField())

        mes_selecionado = self.request.GET.get('mes')

        if mes_selecionado != '0': 
            pacientes = Paciente.objects.filter(data_nascimento__month=mes_selecionado).annotate(day=day_expr, month=month_expr).order_by('month', 'day')
        else:
            pacientes = Paciente.objects.annotate(day=day_expr, month=month_expr).order_by('month', 'day')

        return pacientes

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        valor = '0'
        titulo = 'Aniversários dos Pacientes'
        opcao = 'Filtrar pelo mês'
        aviso = 'Ainda não há pacientes cadastrados'
        mes_selecionado = self.request.GET.get('mes')

        if mes_selecionado:
            mes = nome_mes(mes_selecionado)
            if mes != 'None':
                valor = mes_selecionado
                opcao = mes
                titulo = f'Aniversários dos Pacientes em {opcao}'
                aviso = f'Nenhum paciente faz aniversário no mês de {opcao}'
            else:
                opcao = 'Todos'

        context['valor'] = valor
        context['opcao'] = opcao
        context['aviso'] = aviso
        context['titulo'] = titulo
        return context
    
    def render_to_response(self, context, **response_kwargs):
        return self.render_to_pdf(context)

    def render_to_pdf(self, context):
        template = get_template(self.template_name)
        html_content = template.render(context)

        wkhtmltopdf_path = get_wkhtmltopdf_path()
        pdfkit_config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)

        try:
            pdf_file = pdfkit.from_string(html_content, False, configuration=pdfkit_config)
            response = HttpResponse(pdf_file, content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename="Aniversarios_Pacientes.pdf"'

            return response
        except Exception as e:
            logger.error(f"Erro ao gerar PDF: {e}")
            return HttpResponse(f"Erro ao gerar PDF: {e}", status=500)
        
    
class Agendamentos_PDF(AgendamentoList):
    template_name = 'relatorios/agendamentos_pdf.html'
    
    def render_to_response(self, context, **response_kwargs):
        return self.render_to_pdf(context)

    def render_to_pdf(self, context):
        template = get_template(self.template_name)
        html_content = template.render(context)

        wkhtmltopdf_path = get_wkhtmltopdf_path()
        pdfkit_config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)

        titulo = 'Agendamentos'
        data_agend = self.request.GET.get('data-pesquisada')
        especialidade_agend = self.request.GET.get('especialidade-pesquisada')

        if data_agend and data_agend != '' and data_agend != 'None' and especialidade_agend and especialidade_agend != '' and especialidade_agend != 'None':
            data = datetime.strptime(data_agend, '%Y-%m-%d').strftime('%d/%m/%Y')
            titulo = f'Agendamentos do dia {data} para {especialidade_agend}s'
        elif especialidade_agend and especialidade_agend != '' and especialidade_agend != 'None':
            titulo = f'Agendamentos para {especialidade_agend}s'
        if data_agend and data_agend != '' and data_agend != 'None':
            data = datetime.strptime(data_agend, '%Y-%m-%d').strftime('%d/%m/%Y')
            titulo = f'Agendamentos do dia {data}'

        # Configura a orientação para horizontal
        options = {'page-size': 'A4', 'orientation': 'Landscape'}

        try:
            pdf_file = pdfkit.from_string(html_content, False, configuration=pdfkit_config, options=options)
            response = HttpResponse(pdf_file, content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename="{}.pdf"'.format(titulo)

            return response
        except Exception as e:
            logger.error(f"Erro ao gerar PDF: {e}")
            return HttpResponse(f"Erro ao gerar PDF: {e}", status=500)
    

class RelatorioFinanceiroPDF(RelatorioFinanceiro):
    template_name = "relatorios/relatorio_financeiro_pdf.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        titulo = 'Relatório Financeiro Geral'
        periodo_inicial = self.request.GET.get('periodo-inicial')
        periodo_final = self.request.GET.get('periodo-final')

        if periodo_inicial and periodo_final and periodo_inicial != '' and periodo_final != '' and periodo_inicial != 'None' and periodo_final != 'None':
            data_inicial = datetime.strptime(periodo_inicial, '%Y-%m-%d').strftime('%d/%m/%Y')
            data_final = datetime.strptime(periodo_final, '%Y-%m-%d').strftime('%d/%m/%Y')
            titulo = f'Relatório Financeiro de {data_inicial} a {data_final}'

        context['titulo'] = titulo
        return context


    def render_to_response(self, context, **response_kwargs):
        return self.render_to_pdf(context)

    def render_to_pdf(self, context):
        template = get_template(self.template_name)
        html_content = template.render(context)
        periodo_inicial = 'None' 
        periodo_final = 'None'

        wkhtmltopdf_path = get_wkhtmltopdf_path()
        pdfkit_config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)

        titulo = 'Relatório Financeiro Geral'
        periodo_inicial = self.request.GET.get('periodo-inicial')
        periodo_final = self.request.GET.get('periodo-final')

        if periodo_inicial and periodo_final and periodo_inicial != '' and periodo_final != '' and periodo_inicial != 'None' and periodo_final != 'None':
            data_inicial = datetime.strptime(periodo_inicial, '%Y-%m-%d').strftime('%d/%m/%Y')
            data_final = datetime.strptime(periodo_final, '%Y-%m-%d').strftime('%d/%m/%Y')
            titulo = f'Relatório Financeiro de {data_inicial} a {data_final}'

        options = {'page-size': 'A4'}

        try:
            pdf_file = pdfkit.from_string(html_content, False, configuration=pdfkit_config, options=options)
            response = HttpResponse(pdf_file, content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename="{}.pdf"'.format(titulo)

            return response
        except Exception as e:
            logger.error(f"Erro ao gerar PDF: {e}")
            return HttpResponse(f"Erro ao gerar PDF: {e}", status=500)


class GerarReciboPDF(LoginRequiredMixin, GrupoMixin, TemplateView):
    login_url = reverse_lazy('login')
    template_name = "relatorios/recibo_pdf.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        pk = self.kwargs.get('pk')
        agendamento = Agendamento.objects.get(pk=pk)
        titulo = ''

        if agendamento.tipo_agendamento == 'Consulta':
            titulo = 'Recibo de Consulta'
        else:
            titulo = 'Recibo de Procedimento'

        context['titulo'] = titulo
        context['agendamento'] = agendamento

        return context

    def render_to_response(self, context, **response_kwargs):
        return self.render_to_pdf(context)

    def render_to_pdf(self, context):
        template = get_template(self.template_name)
        html_content = template.render(context)

        wkhtmltopdf_path = get_wkhtmltopdf_path()
        pdfkit_config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)

        pk = self.kwargs.get('pk')
        agendamento = Agendamento.objects.get(pk=pk)
        titulo = ''

        if agendamento.tipo_agendamento == 'Consulta':
            titulo = 'Recibo de Consulta'
        else:
            titulo = 'Recibo de Procedimento'

        options = {'page-size': 'A5', 'orientation': 'Landscape'}

        try:
            pdf_file = pdfkit.from_string(html_content, False, configuration=pdfkit_config, options=options)
            response = HttpResponse(pdf_file, content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename="{}.pdf"'.format(titulo)

            return response
        except Exception as e:
            logger.error(f"Erro ao gerar PDF: {e}")
            return HttpResponse(f"Erro ao gerar PDF: {e}", status=500)
        

class ProntuarioPDF(MostrarProntuario):
    template_name = "relatorios/prontuario_pdf.html"

    def render_to_response(self, context, **response_kwargs):
        return self.render_to_pdf(context)

    def render_to_pdf(self, context):
        template = get_template(self.template_name)
        html_content = template.render(context)

        wkhtmltopdf_path = get_wkhtmltopdf_path()
        pdfkit_config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)

        pk = self.kwargs.get('pk')
        prontuario = Prontuario.objects.get(pk=pk)
        paciente = prontuario.paciente

        options = {'page-size': 'A4'}

        try:
            pdf_file = pdfkit.from_string(html_content, False, configuration=pdfkit_config, options=options)
            response = HttpResponse(pdf_file, content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename="Prontuário - {}.pdf"'.format( paciente)

            return response
        except Exception as e:
            logger.error(f"Erro ao gerar PDF: {e}")
            return HttpResponse(f"Erro ao gerar PDF: {e}", status=500)

'''class GerarFichaPacientePDF(View, GeradorDePDF):
    def get_nome_arquivo(self):
        paciente = self.data.get('paciente')
        return f'Ficha do Paciente - {paciente.nome_completo}.pdf'
    
    def get_titulo_PDF(self):
        return 'SISMED - Ficha de Cadastro do Paciente'
    
    def get_titulo(self):
        return 'Ficha de Cadastro do Paciente'

    def adicionar_conteudo(self, pdf):
        paciente = self.data.get('paciente')
        x, y = 65, 700
        altura_disponivel = 700  # Altura disponível na página, ajuste conforme necessário
        tamanho_linha = 20  # Tamanho da linha da fonte, ajuste conforme necessário

        # Exemplo de dados
        dados = [
            f'Nome: {paciente.nome_completo}',
            f'Data de Nascimento: {paciente.data_nascimento.strftime("%d/%m/%Y")}',
            f'Idade: {paciente.get_idade()} anos',
            f'RG: {paciente.rg}',
            f'CPF: {paciente.cpf}',
            f'Sexo: {paciente.sexo}',
            f'Telefone: {paciente.telefone}',
            f'Email: {paciente.email}',
            f'Rua: {paciente.endereco.rua}',
            f'Número: {paciente.endereco.numero}',
            f'Bairro: {paciente.endereco.bairro}',
            f'Cidade: {paciente.endereco.cidade}',
            f'Informacoes Médicas: {paciente.informacoes_medicas}',
            f'Data de Cadastro: {paciente.data_cadastro.strftime("%d/%m/%Y")}',
        ]

        for dado in dados:
            # Verifica se há espaço suficiente para o próximo item
            if y - tamanho_linha < 30:
                pdf.showPage()  # Inicia uma nova página
                y = altura_disponivel  # Reinicia a posição Y
                self.adicionar_cabecalho(pdf, self.get_titulo())  # Adiciona o cabeçalho na nova página

            # Adiciona o dado à página
            pdf.drawString(x, y - 5, dado)
            y -= tamanho_linha  # Atualiza a posiçã

    def get(self, request, *args, **kwargs):
        paciente = get_object_or_404(Paciente, pk=kwargs['pk'])
        self.data = {'paciente': paciente}
        return self.gerarPDF()'''


class GerarFichaPaciente(GroupRequiredMixin, LoginRequiredMixin, GrupoMixin, DetailView):
    login_url = reverse_lazy('login')
    group_required = u'Administrador'
    model = Paciente
    template_name = 'relatorios/ficha_paciente.html'


class GerarFichaFuncionario(GroupRequiredMixin, LoginRequiredMixin, GrupoMixin, DetailView):
    login_url = reverse_lazy('login')
    group_required = u'Administrador'
    model = Funcionario
    template_name = 'relatorios/ficha_funcionario.html'





