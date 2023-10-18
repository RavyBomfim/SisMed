from django.contrib import admin

# Register your models here.
from.models import AgendaMedico, Cargo, Funcionario, Especialidade, HorarioAtendimento, Medico, Paciente

admin.site.register(Cargo)
admin.site.register(Funcionario)
admin.site.register(Especialidade)
admin.site.register(Medico)
admin.site.register(Paciente)
admin.site.register(AgendaMedico)
admin.site.register(HorarioAtendimento)

admin.site.site_header = 'Administração SisMed'