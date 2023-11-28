from django.http import HttpResponse
'''from reportlab.pdfgen import canvas
from django.contrib.staticfiles import finders
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm

class GeradorDePDF:
    def get_nome_arquivo(self):
        raise NotImplementedError("A subclasse deve implementar o método get_nome_arquivo")
    
    def get_titulo_PDF(self):
        raise NotImplementedError("A subclasse deve implementar o método get_titulo_PDF")

    def get_titulo(self, titulo):
        raise NotImplementedError("A subclasse deve implementar o método get_titulo")
    
    def adicionar_cabecalho(self, pdf, titulo):
        rect_x, rect_y, rect_width, rect_height = 65, 720, 463, 28

        image_path = finders.find('img/Sismed-img.jpg')
        pdf.drawInlineImage(image_path, 22*mm, 760, width=100, height=40)
        pdf.setFont("Helvetica", 10)
        pdf.setFillColor('#2d2c2c')
        pdf.drawString(170, 783, 'Rua Flores, nº 857 - Campos, Camões/MS')
        pdf.drawString(170, 768, 'Telefone: (45) 4587-6582')
        pdf.setFillAlpha(1)
        pdf.setStrokeColor('#a8ccb6')
        pdf.setFillColor('#a8ccb6')
        pdf.rect(rect_x, rect_y, rect_width, rect_height, fill=True)

        titulo_font_size = 16  # Tamanho da fonte do título
        font_size_padrao = 12

        # Calculando as coordenadas para centralizar o título
        titulo_width = pdf.stringWidth(titulo, "Helvetica-Bold", titulo_font_size)
        titulo_x = rect_x + (rect_width - titulo_width) / 2
        titulo_y = rect_y + (rect_height - titulo_font_size) / 2

        pdf.setFont("Helvetica", titulo_font_size)
        pdf.setFillColorRGB(0, 0, 0)  # Cor do texto (preto)

        # Adicionando o título centralizado
        pdf.drawString(titulo_x, titulo_y, titulo)

        pdf.setFont("Helvetica", font_size_padrao)

    def adicionar_conteudo(self, pdf):
        raise NotImplementedError("A subclasse deve implementar o método adicionar_conteudo")

    def gerarPDF(self):
        resposta = HttpResponse(content_type='application/pdf')
        resposta['Content-Disposition'] = f'inline; filename="{self.get_nome_arquivo()}"'

        pdf = canvas.Canvas(resposta, pagesize=A4)
        pdf.setTitle(self.get_titulo())
        self.adicionar_cabecalho(pdf, self.get_titulo())
        self.adicionar_conteudo(pdf)

        pdf.showPage()
        pdf.save()

        return resposta'''