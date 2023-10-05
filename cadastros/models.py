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
    endereco = models.OneToOneField(Endereco, on_delete=models.PROTECT)
    telefone = models.CharField(max_length=15) 
    email = models.CharField(max_length=50) 
    data_cadastro = models.DateField(verbose_name='Data de Cadastro') 
    informacoes_medicas = models.TextField(verbose_name='Informações Médicas')
    foto =  models.ImageField(upload_to='fotos_pacientes', blank=True, null=True)

    def __str__(self):
        return f'{self.nome_completo} {self.data_nascimento} {self.rg} {self.cpf} {self.endereco} {self.telefone} {self.email} {self.data_cadastro} {self.informacoes_medicas}'


class Tipo_procedimento(models.Model):
    nome_procedimento = models.CharField(max_length=50, verbose_name='Nome do Procedimento'),
    valor = models.DecimalField(decimal_places=2, max_digits=8)

    def __str__(self):
        return f'{self.nome_procedimento} {self.valor}'


class Anotacao(models.Model):
    nota_medico = models.TextField(verbose_name="Nota")

    def __str__(self):
        return f'{self.nota_medico}'


class Prontuario(models.Model):
    data_criacao = models.DateField()
    pertence = models.OneToOneField(Paciente, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.data_criacao} {self.pertence}'

class Procedimento(models.Model):
    prontuario = models.ForeignKey(Prontuario, on_delete=models.PROTECT)
    tipo_procedimento = models.ForeignKey(Tipo_procedimento, verbose_name='Tipo de Procedimento', on_delete=models.PROTECT)
    data = models.DateField()
    hora = models.TimeField()
    medico =  models.CharField(max_length=100, verbose_name='Médico')
    nome_paciente = models.CharField(max_length=100, verbose_name='Nome do Paciente')
    codigo = models.CharField(max_length=15)
    cpf = models.CharField(max_length=14, verbose_name='CPF')
    observacao = models.OneToOneField(Anotacao, null=True, blank=True, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.tipo_procedimento} {self.data} {self.hora} {self.nome_paciente} {self.medico} {self.codigo} {self.observacao}'