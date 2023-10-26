from django.contrib import admin

# Register your models here.
from.models import AgendaMedico, AgendamentoConsulta, Cargo, Funcionario, Especialidade, HorarioAtendimento, HorarioMedico, Medico, Paciente

admin.site.register(Cargo)
admin.site.register(Funcionario)
admin.site.register(Especialidade)
admin.site.register(Medico)
admin.site.register(Paciente)
admin.site.register(AgendaMedico)
admin.site.register(HorarioAtendimento)
admin.site.register(HorarioMedico)
admin.site.register(AgendamentoConsulta)

admin.site.site_header = 'Administração SisMed'