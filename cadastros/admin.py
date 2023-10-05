from django.contrib import admin

# Register your models here.
from.models import Cargo, Funcionario, Especialidade, Medico

admin.site.register(Cargo)
admin.site.register(Funcionario)
admin.site.register(Especialidade)
admin.site.register(Medico)