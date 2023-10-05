from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
class IndexView(TemplateView):
    template_name = "paginas/index.html"

    def get(self, request, *args, **kwargs):
        user = self.request.user
        is_admin = user.groups.filter(name='Administrador').exists
        is_medico = user.groups.filter(name='Administrador').exists
        return render(request, self.template_name, {'is_admin': is_admin, 'is_medico': is_medico})
