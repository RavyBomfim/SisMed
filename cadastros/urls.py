from django.urls import path
from .views import AgendaDetail, AniversariosPacientesList, CargoCreate, CargoList, CargoUpdate, CargoDelete, EspecialidadeCreate, EspecialidadeDelete, EspecialidadeList, EspecialidadeUpdate, FuncionarioCreate, FuncionarioDelete, FuncionarioDetail, FuncionarioList, FuncionarioUpdate, HorarioCreate, HorarioDelete, HorarioUpdate, MedicoCreate, MedicoDelete, MedicoDetail, MedicoList, MedicoUpdate, PacienteCreate, PacienteDelete, PacienteDetail, PacienteList, PacienteUpdate, PacientesMedico, ProcedimentoCreate, ProcedimentoDelete, ProcedimentoList, ProcedimentoUpdate

urlpatterns = [
    path('cadastrar/cargo', CargoCreate.as_view(), name='cadastrar-cargo'),
    path('cadastrar/funcionario', FuncionarioCreate.as_view(), name='cadastrar-funcionario'),
    path('cadastrar/especialidade', EspecialidadeCreate.as_view(), name='cadastrar-especialidade'),
    path('cadastrar/medico', MedicoCreate.as_view(), name='cadastrar-medico'),
    path('cadastrar/paciente', PacienteCreate.as_view(), name='cadastrar-paciente'),
    path('cadastar/procedimento', ProcedimentoCreate.as_view(), name='cadastrar-procedimento'),
    
    path('cadastrar/horario/agenda<int:pk>', HorarioCreate.as_view(), name='cadastrar-horario'),
    path('editar/agenda<int:fk>/horario<int:pk>', HorarioUpdate.as_view(), name='editar-agenda'),
    path('excluir/horario<int:pk>/agenda<int:fk>', HorarioDelete.as_view(), name='excluir-horario'),

    path('editar/cargo/<int:pk>', CargoUpdate.as_view(), name='editar-cargo'),
    path('editar/funcionario/<int:pk>', FuncionarioUpdate.as_view(), name='editar-funcionario'),
    path('editar/especialidade/<int:pk>', EspecialidadeUpdate.as_view(), name='editar-especialidade'),
    path('editar/medico/<int:pk>', MedicoUpdate.as_view(), name='editar-medico'),
    path('editar/paciente/<int:pk>', PacienteUpdate.as_view(), name='editar-paciente'),
    path('editar/procedimento/<int:pk>', ProcedimentoUpdate.as_view(), name='editar-procedimento'),

    path('excluir/cargo/<int:pk>', CargoDelete.as_view(), name='excluir-cargo'),
    path('excluir/funcionario/<int:pk>', FuncionarioDelete.as_view(), name='excluir-funcionario'),
    path('excluir/especialidade/<int:pk>', EspecialidadeDelete.as_view(), name='excluir-especialidade'),
    path('excluir/medico/<int:pk>', MedicoDelete.as_view(), name='excluir-medico'),
    path('excluir/paciente/<int:pk>', PacienteDelete.as_view(), name='excluir-paciente'),
    path('excluir/procedimento/<int:pk>', ProcedimentoDelete.as_view(), name='excluir-procedimento'),
    #path('excluir/endereco/<int:pk>', EnderecoDelete.as_view(), name='excluir-endereco'),

    path('listar/cargos', CargoList.as_view(), name='listar-cargos'),
    path('listar/funcionarios', FuncionarioList.as_view(), name='listar-funcionarios'),
    path('listar/especialidades', EspecialidadeList.as_view(), name='listar-especialidades'),
    path('listar/medicos', MedicoList.as_view(), name='listar-medicos'),
    path('listar/pacientes', PacienteList.as_view(), name='listar-pacientes'),
    path('listar/pacientes/medico', PacientesMedico.as_view(), name='listar-pacientes-medico'),
    path('aniversarios/pacientes', AniversariosPacientesList.as_view(), name='aniversarios-pacientes'),
    path('aniversarios/mes', AniversariosPacientesList.as_view(), name='aniversarios-mes'),
    path('listar/procedimentos', ProcedimentoList.as_view(), name='listar-procedimentos'),

    path('dados/funcionario/<int:pk>', FuncionarioDetail.as_view(), name='dados-funcionario'),
    path('dados/medico/<int:pk>', MedicoDetail.as_view(), name='dados-medico'),
    path('dados/paciente/<int:pk>', PacienteDetail.as_view(), name='dados-paciente'),
    path('dados/agenda/<int:pk>', AgendaDetail.as_view(), name='dados-agenda'),
]