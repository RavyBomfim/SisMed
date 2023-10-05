from django.db import models

# Create your models here.

class Endereco(models.Model):
    rua = models.CharField(max_length=50)
    numero = models.IntegerField(null=True, blank=True, verbose_name='Número')
    bairro = models.CharField(max_length=50)
    cidade = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.rua} {self.numero} {self.bairro} {self.cidade}'


class Cargo(models.Model):
    nome_cargo = models.CharField(max_length=50, unique=True, verbose_name='Nome do cargo')
    salario = models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Salário')

    def __str__(self):
        return f'{self.nome_cargo} {self.salario}'


class Funcionario(models.Model):
    nome_completo = models.CharField(max_length=100, verbose_name='Nome Completo')
    data_nascimento = models.DateField(verbose_name='Data de Nascimento')
    rg = models.CharField(max_length=13, verbose_name='RG', unique=True)
    cpf = models.CharField(max_length=14, verbose_name='CPF', unique=True)
    endereco = models.OneToOneField(Endereco, null=True, on_delete=models.PROTECT)
    telefone = models.CharField(max_length=15, unique=True) 
    email = models.CharField(max_length=50, unique=True) 
    """data_admissao = models.DateField(verbose_name='Data de Admissão')
    data_demissao = models.DateField(null=True, blank=True, verbose_name='Data de Demissão')"""
    data_cadastro = models.DateField(verbose_name='Data de Cadastro')
    cargo = models.ForeignKey(Cargo, on_delete=models.PROTECT) 
    foto =  models.ImageField(upload_to='fotos_funcionarios', blank=True, null=True)

    def __str__(self):
        return f'{self.nome_completo} {self.data_nascimento} {self.rg} {self.cpf} {self.endereco} {self.telefone} {self.email} {self.data_cadastro} {self.cargo}'

class Especialidade(models.Model):
    especialidade = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return f'{self.especialidade}'


class Medico(models.Model):
    nome_completo = models.CharField(max_length=100, verbose_name='Nome Completo')
    data_nascimento = models.DateField(verbose_name='Data de Nascimento')
    rg = models.CharField(max_length=13, verbose_name='RG', unique=True)
    cpf = models.CharField(max_length=14, verbose_name='CPF', unique=True)
    endereco = models.OneToOneField(Endereco, null=True, on_delete=models.PROTECT)
    telefone = models.CharField(max_length=15, unique=True) 
    email = models.CharField(max_length=50, unique=True) 
    data_cadastro = models.DateField(verbose_name='Data de Cadastro') 
    especialidade = models.ForeignKey(Especialidade, on_delete=models.PROTECT)
    foto =  models.ImageField(upload_to='fotos_medicos', blank=True, null=True)

    def __str__(self):
        return f'{self.nome_completo} {self.data_nascimento} {self.rg} {self.cpf} {self.endereco} {self.telefone} {self.email} {self.data_cadastro} {self.especialidade}'


class Paciente(models.Model):
    nome_completo = models.CharField(max_length=100, verbose_name='Nome Completo')
    data_nascimento = models.DateField(verbose_name='Data de Nascimento')
    rg = models.CharField(max_length=13, verbose_name='RG', unique=True)
    cpf = models.CharField(max_length=14, verbose_name='CPF', unique=True)
    endereco = models.OneToOneField(Endereco, null=True, on_delete=models.PROTECT)
    telefone = models.CharField(max_length=15) 
    email = models.CharField(max_length=50) 
    data_cadastro = models.DateField(verbose_name='Data de Cadastro') 
    informacoes_medicas = models.TextField(verbose_name='Informações Médicas')
    foto =  models.ImageField(upload_to='fotos_pacientes', blank=True, null=True)

    def __str__(self):
        return f'{self.nome_completo} {self.data_nascimento} {self.rg} {self.cpf} {self.endereco} {self.telefone} {self.email} {self.data_cadastro} {self.informacoes_medicas}'


"""class Anotacao(models.Model):
    nota_medico = models.TextField(verbose_name="Nota")

    def __str__(self):
        return f'{self.nota_medico}'
"""

class Prontuario(models.Model):
    data_criacao = models.DateField()
    paciente = models.OneToOneField(Paciente, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.data_criacao} {self.pertence}'


class Procedimento(models.Model):
    codigo = models.CharField(max_length=15)
    descricao = models.CharField(max_length=50, null=True, verbose_name='Descricão')
    valor = models.DecimalField(decimal_places=2, max_digits=8, null=True)
    observacao = models.TextField(null=True, verbose_name='Observações Gerais Sobre o Procedimento')

    def __str__(self):
        return f'{self.codigo} {self.descricao} {self.valor} {self.observacao}' 
    

class Agendamento_Consulta(models.Model):
    tipo_opcoes = (('Plano', 'Plano'), ('Particular', 'Particular'))

    codigo = models.CharField(max_length=15)
    agendamento = models.DateTimeField()
    paciente = models.ForeignKey(Paciente, on_delete=models.PROTECT)
    medico = models.ForeignKey(Medico, on_delete=models.PROTECT)
    tipo_consulta = models.CharField(max_length=10, choices=tipo_opcoes)
    retorno = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.codigo} {self.agendamento} {self.paciente} {self.medico} {self.tipo_consulta} {self.retorno}' 