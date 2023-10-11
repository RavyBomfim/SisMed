from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class IndexView(LoginRequiredMixin, TemplateView):

    login_url = reverse_lazy('login')
    template_name = "paginas/index.html"

    def get(self, request, *args, **kwargs):
        user = self.request.user
        is_admin = user.groups.filter(name='Administrador').exists
        is_medico = user.groups.filter(name='Administrador').exists
        return render(request, self.template_name, {'is_admin': is_admin, 'is_medico': is_medico})
