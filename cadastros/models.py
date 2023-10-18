from django.db import models
from datetime import date
from django.contrib.auth.models import User

# Create your models here.
sexo_opcoes = (('M', 'Masculino'), ('F', 'Feminino'))
boolean_opcoes = (('True', 'Sim'), ('False', 'Não'))

class Endereco(models.Model):
    rua = models.CharField(max_length=50)
    numero = models.IntegerField(null=True, blank=True, verbose_name='Número')
    bairro = models.CharField(max_length=50)
    cidade = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.rua} {self.numero} {self.bairro} {self.cidade}'


class Cargo(models.Model):
    nome_cargo = models.CharField(max_length=50, unique=True, verbose_name='Nome do cargo')
    salario = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Salário')

    def __str__(self):
        return f'{self.nome_cargo} {self.salario}'


class Funcionario(models.Model):
    nome_completo = models.CharField(max_length=100, verbose_name='Nome Completo')
    data_nascimento = models.DateField(verbose_name='Data de Nascimento')
    rg = models.CharField(max_length=13, verbose_name='RG', unique=True)
    cpf = models.CharField(max_length=14, verbose_name='CPF', unique=True)
    sexo = models.CharField(max_length=1, choices=sexo_opcoes, null=True) 
    endereco = models.OneToOneField(Endereco, null=True, on_delete=models.PROTECT)
    telefone = models.CharField(max_length=15, unique=True) 
    email = models.CharField(max_length=50, unique=True) 
    data_admissao = models.DateField(null=True, verbose_name='Data de Admissão')
    data_demissao = models.DateField(null=True, blank=True, verbose_name='Data de Demissão')
    cargo = models.ForeignKey(Cargo, on_delete=models.PROTECT) 
    foto =  models.ImageField(upload_to='fotos_funcionarios', blank=True, null=True)
    usuario = models.OneToOneField(User, null=True, blank=True, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'{self.nome_completo}'

    """def __str__(self):
        return f'{self.nome_completo} {self.data_nascimento} {self.rg} {self.cpf} {self.endereco} {self.telefone} {self.email} {self.data_admissao} {self.data_demissao} {self.cargo}'"""


class Especialidade(models.Model):
    especialidade = models.CharField(max_length=30, unique=True)
    valor_consulta = models.DecimalField(max_digits=8, decimal_places=2, null=True)

    def __str__(self):
        return f'{self.especialidade}'


class Medico(models.Model):
    nome_completo = models.CharField(max_length=100, verbose_name='Nome Completo')
    data_nascimento = models.DateField(verbose_name='Data de Nascimento')
    rg = models.CharField(max_length=13, verbose_name='RG', unique=True)
    cpf = models.CharField(max_length=14, verbose_name='CPF', unique=True)
    crm = models.CharField(null=True, max_length=14, verbose_name='CRM', unique=True)
    sexo = models.CharField(max_length=1, choices=sexo_opcoes, null=True) 
    endereco = models.OneToOneField(Endereco, null=True, on_delete=models.PROTECT)
    telefone = models.CharField(max_length=15, unique=True) 
    email = models.CharField(max_length=50, unique=True) 
    data_cadastro = models.DateField(verbose_name='Data de Cadastro') 
    especialidade = models.ForeignKey(Especialidade, on_delete=models.PROTECT)
    foto =  models.ImageField(upload_to='fotos_medicos', blank=True, null=True)
    usuario = models.OneToOneField(User, null=True, on_delete=models.DO_NOTHING)

    def save(self, *args, **kwargs):
        if not self.data_cadastro:
            self.data_cadastro = date.today()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.nome_completo} - {self.especialidade}'

    """def __str__(self):
        return f'{self.nome_completo} {self.data_nascimento} {self.rg} {self.cpf} {self.crm} {self.endereco} {self.telefone} {self.email} {self.data_cadastro} {self.especialidade}'"""


class Paciente(models.Model):
    nome_completo = models.CharField(max_length=100, verbose_name='Nome Completo')
    data_nascimento = models.DateField(verbose_name='Data de Nascimento')
    rg = models.CharField(max_length=13, verbose_name='RG', unique=True)
    cpf = models.CharField(max_length=14, verbose_name='CPF', unique=True)
    sexo = models.CharField(max_length=1, choices=sexo_opcoes, null=True) 
    endereco = models.OneToOneField(Endereco, null=True, on_delete=models.PROTECT)
    telefone = models.CharField(max_length=15) 
    email = models.CharField(max_length=50) 
    data_cadastro = models.DateField(verbose_name='Data de Cadastro') 
    informacoes_medicas = models.TextField(verbose_name='Informações Médicas')
    foto =  models.ImageField(upload_to='fotos_pacientes', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.data_cadastro:
            self.data_cadastro = date.today()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.nome_completo}'

    """def __str__(self):
        return f'{self.nome_completo} {self.data_nascimento} {self.rg} {self.cpf} {self.endereco} {self.telefone} {self.email} {self.data_cadastro} {self.informacoes_medicas}'"""


class Nota(models.Model):
    nota_medico = models.TextField(verbose_name="Nota")
    paciente = models.ForeignKey(Paciente, on_delete=models.PROTECT)
    medico = models.ForeignKey(Medico, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.nota_medico} {self.paciente} {self.medico}'
    

class HorarioAtendimento(models.Model):
    horario_atendimento = models.TimeField(unique=True)

    def __str__(self):
        return f'{self.horario_atendimento}'


class AgendaMedico(models.Model):
    medico = models.OneToOneField(Medico, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.medico}'


class HorarioMedico(models.Model):
    agenda = models.ForeignKey(AgendaMedico, null=True, on_delete=models.CASCADE)
    dia_semana = models.IntegerField(choices=[(1, 'Segunda-feira'), (2, 'Terça-feira'), (3, 'Quarta-feira'), (4, 'Quinta-feira'), (5, 'Sexta-feira'), (6, 'Sábado')])
    horario_inicial_manha = models.TimeField(null=True, blank=True)
    horario_final_manha = models.TimeField(null=True, blank=True)
    horario_inicial_tarde = models.TimeField(null=True, blank=True)
    horario_final_tarde = models.TimeField(null=True, blank=True)


class HorarioAgenda(models.Model):
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    data = models.DateField()
    horario = models.TimeField()
    disponivel = models.BooleanField(default=True)


class Prontuario(models.Model):
    data_criacao = models.DateField()
    paciente = models.OneToOneField(Paciente, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.data_criacao} {self.paciente}'


class Procedimento(models.Model): 
    codigo = models.CharField(max_length=15)
    descricao = models.CharField(max_length=50, null=True, verbose_name='Descricão')
    valor = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    observacao = models.TextField(null=True, verbose_name='Observações Gerais Sobre o Procedimento')

    def __str__(self):
        return f'{self.codigo}' 
    

class ProcedimentoAgendado(models.Model):
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    procedimento = models.ForeignKey(Procedimento, on_delete=models.CASCADE)
    data_hora = models.DateTimeField()

    def __str__(self):
        return f'{self.medico} {self.paciente} {self.procedimento} {self.data_hora}' 
    

class AgendamentoConsulta(models.Model):
    tipo_consulta_opcoes = (('Plano', 'Plano'), ('Particular', 'Particular'))

    codigo = models.CharField(max_length=15)
    data_hora = models.DateTimeField()
    paciente = models.ForeignKey(Paciente, on_delete=models.PROTECT)
    medico = models.ForeignKey(Medico, on_delete=models.PROTECT)
    tipo_consulta = models.CharField(max_length=10, choices=tipo_consulta_opcoes)
    retorno = models.BooleanField(default=False, choices=boolean_opcoes)
    valor_consulta = models.DecimalField(max_digits=8, decimal_places=2, editable=False)

    def __str__(self):
        return f'{self.codigo} {self.data_hora} {self.paciente} {self.medico} {self.tipo_consulta} {self.retorno} {self.valor_consulta}' 
