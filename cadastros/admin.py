from django.contrib import admin

# Register your models here.
from.models import Agendamento, Cargo, Especialidade, HorarioAtendimento, Medico, Procedimento, Prontuario

admin.site.register(Cargo)
admin.site.register(Especialidade)
'''admin.site.register(Medico)'''
admin.site.register(HorarioAtendimento)
'''admin.site.register(Prontuario)'''

admin.site.site_header = 'Administração SisMed'