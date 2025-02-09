# SisMed
![Logo do Sismed](https://github.com/user-attachments/assets/16886df0-0f7c-4bea-a18c-03778d89be37)
 Sistema de Clínica Médica

<hr>


### Tópicos

* [Descrição do projeto](#descrição-do-projeto) 
* [Funcionalidades](#funcionalidades)
* [Tecnologias utilizadas](#tecnologias-utilizadas)
* [Acesso ao projeto](#acesso-ao-projeto)
* [Como utilizá-lo](#como-utilizar)
* [Desenvolvedores](#desenvolvedores)

<hr>


<h2 id="descrição-do-projeto">Descrição do projeto</h2>

Sistema de Clínica Médica Completo em Django.
Projeto requisitado na disciplina de Programação Web II da graduação em Análise e Desenvolvimento de Sistemas.

O Sistema possui níveis e controle de acesso, com funcionaldades e acesso à informações específicas de acordo com o tipo de usuário logado (Administrador ou Médico).

<h2 id="funcionalidades">Funcionalidades</h2>

<h4>Administradores podem:</h4>

- [x] `Funcionalidade 1:` Cadastrar Cargo
- [x] `Funcionalidade 2:` Cadastrar Especialidade
- [x] `Funcionalidade 3:` Cadastrar Funcionário
- [x] `Funcionalidade 4:` Cadastrar Médico
- [x] `Funcionalidade 5:` Cadastrar Paciente
- [x] `Funcionalidade 6:` Cadastrar Procedimento
- [x] `Funcionalidade 7:` Cadastrar Usuário
- [x] `Funcionalidade 8:` Agendar Atendimento (Consulta/Procedimento)
- [x] `Funcionalidade 9:` Listar Cargos
- [x] `Funcionalidade 10:` Listar Especialidades
- [x] `Funcionalidade 11:` Listar Funcionários
- [x] `Funcionalidade 12:` Pesquisar Funcionários pelo nome
- [x] `Funcionalidade 13:` Ver detalhes de cadastro de Funcionário
- [x] `Funcionalidade 14:` Imprimir Dados do Funcionário em PDF
- [x] `Funcionalidade 15:` Listar Médicos
- [x] `Funcionalidade 16:` Pesquisar Médicos pelo nome
- [x] `Funcionalidade 17:` Ver detalhes de cadastro de Médico
- [x] `Funcionalidade 18:` Listar Pacientes
- [x] `Funcionalidade 19:` Pesquisar Pacientes pelo nome
- [x] `Funcionalidade 20:` Visualizar Aniversários dos Pacientes
- [x] `Funcionalidade 21:` Filtrar Aniversários pelo mês de nascimento
- [x] `Funcionalidade 22:` Imprimir Aniversários em PDF
- [x] `Funcionalidade 23:` Ver detalhes de cadastro de Paciente
- [x] `Funcionalidade 24:` Imprimir Ficha do Paciente em PDF
- [x] `Funcionalidade 25:` Acessar Prontuário do Paciente
- [x] `Funcionalidade 26:` Imprimir Prontuário em PDF
- [x] `Funcionalidade 27:` Listar Procedimentos
- [x] `Funcionalidade 28:` Acessar Agendamentos
- [x] `Funcionalidade 29:` Ver detalhes de Agendamento
- [x] `Funcionalidade 30:` Acessar Pacientes do Dia
- [x] `Funcionalidade 31:` Editar Cargo
- [x] `Funcionalidade 32:` Editar Especialidade
- [x] `Funcionalidade 33:` Editar Funcionário
- [x] `Funcionalidade 34:` Editar Médico
- [x] `Funcionalidade 35:` Editar Paciente
- [x] `Funcionalidade 36:` Editar Procedimento
- [x] `Funcionalidade 37:` Editar Agendamento
- [x] `Funcionalidade 38:` Excluir Cargo
- [x] `Funcionalidade 39:` Excluir Especialidade
- [x] `Funcionalidade 40:` Excluir Cadastro de Funcionário
- [x] `Funcionalidade 41:` Excluir Cadastro de Médico
- [x] `Funcionalidade 42:` Excluir Cadastro de Paciente
- [x] `Funcionalidade 43:` Excluir Procedimento
- [x] `Funcionalidade 44:` Excluir Agendamento
- [x] `Funcionalidade 45:` Acessar Agenda dos Médicos
- [x] `Funcionalidade 46:` Editar Agendas dos Médicos
- [x] `Funcionalidade 47:` Ver especialidades mais requisitadas
- [x] `Funcionalidade 48:` Gerar Relatório Financeiro Geral mostrando Valores arrecadados por Especialidade e Valor Total arrecadado
- [x] `Funcionalidade 49:` Gerar Relatório Financeiro de um período específico
- [x] `Funcionalidade 50:` Imprimir Relatório Financeiro em PDF
- [x] `Funcionalidade 51:` Imprimir Relatório Financeiro em PDF

<h4>Médicos podem:</h4>

- [x] `Funcionalidade 1:` Acessar a própria Agenda
- [x] `Funcionalidade 2:` Editar a própria Agendas
- [x] `Funcionalidade 3:` Visualizar seus Pacientes do dia
- [x] `Funcionalidade 4:` Visualizar todos os seus Pacientes
- [x] `Funcionalidade 5:` Pesquisar seus Pacientes pelo nome
- [x] `Funcionalidade 6:` Ver detalhes de Cadastro de seus Pacientes
- [x] `Funcionalidade 7:` Imprimir Ficha do Paciente em PDF
- [x] `Funcionalidade 8:` Ver Agendamentos (Consultas/Procedimentos) onde ele (o usuário) é o médico
- [x] `Funcionalidade 9:` Filtrar  Agendamentos por data
- [x] `Funcionalidade 10:` Gerar PDF com os Agendamentos
- [x] `Funcionalidade 11:` Marcar Agendamento (Consulta/Procedimento) como concluído
- [x] `Funcionalidade 12:` Adicionar Informações de Anamnese do Paciente ao concluir consulta
- [x] `Funcionalidade 13:` Acessar Prontuário do Paciente
- [x] `Funcionalidade 14:` Imprimir Prontuário em PDF

<hr>


<h2 id="tecnologias-utilizadas">Tecnologias utilizadas</h2> 

- [x] <img align="center" alt="Logo do HTML" height="30" width="40" src="https://raw.githubusercontent.com/devicons/devicon/master/icons/html5/html5-original.svg">
HTML - Linguagem de marcação

- [x] <img align="center" alt="Logo do CSS" height="30" width="40" src="https://raw.githubusercontent.com/devicons/devicon/master/icons/css3/css3-original.svg">
CSS - Folha de estilos

- [x] <img align="center" alt="Logo do Materialize" height="30" width="40" src="https://github.com/user-attachments/assets/5e117a71-d434-4391-95f3-335a86eb9506"> 
Materialize - Framework Front-end

- [x] <img align="center" alt="Logo do JavaScript" height="30" width="40" src="https://raw.githubusercontent.com/devicons/devicon/master/icons/javascript/javascript-original.svg"> 
JavaScript - Linguagem de Programação Front-end

- [x] <img align="center" alt="Logo do Python" height="30" width="40" src="https://github.com/user-attachments/assets/3c6bc876-ce1b-492f-878f-08fc23c50217"> 
Python - Linguagem de Programação Back-end

- [x] <img align="center" alt="Logo do Django" height="30" width="40" src="https://github.com/user-attachments/assets/a343311c-6fd4-4436-b88f-df62c2844339"> 
Django - Framework Web

<hr>


<h2 id="acesso-ao-projeto">Acesso ao projeto</h2>

<p>Você pode acessar o código fonte do projeto ou baixá-lo clicando nos links abaixo:<a/> <br>

- <a href="https://github.com/RavyBomfim/SisMed">Acessar o código fonte do projeto<a/> <br>
- <a href="https://github.com/RavyBomfim/SisMed/archive/refs/heads/main.zip">Baixar Projeto<a/>

<hr>


<h2 id="como-utilizar">Como utilizá-lo❔</h2>

<p></p>

<hr>

<h2 id="desenvolvedores">Desenvolvedores</h2>

| <a href="https://github.com/RavyBomfim"> <img alt="Foto de Ravieli" src="https://github.com/user-attachments/assets/ee73852a-a805-4814-b988-8b1cca7a23ca" width=110> <br> Ravieli Bomfim <a/> <br> Front e Back-end | <a href="https://github.com/BrianOrmund"> <img alt="Foto de Brian" src="https://github.com/user-attachments/assets/33703dde-49a0-4935-9d9a-5a3756310cfc" width=110> <br> Brian Ormund <a/>  <br> Front-end |
--- | --- |
