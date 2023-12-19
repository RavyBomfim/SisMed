from django.contrib import admin

# Register your models here.
from.models import Funcionario, HorarioAtendimento

admin.site.register(HorarioAtendimento)
admin.site.register(Funcionario)

admin.site.site_header = 'Administração SisMed'