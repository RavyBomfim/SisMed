from django.urls import path
from django.contrib.auth import views as auth_views
from usuarios.views import UsuarioCreate, UsuarioList

urlpatterns = [
    path('', auth_views.LoginView.as_view(
        template_name='usuarios/login.html'
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        template_name='usuarios/login.html'
    ), name='logout'),
    path('login/', auth_views.LoginView.as_view(
        template_name='usuarios/login.html'
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        template_name='usuarios/login.html'
    ), name='logout'),

    path('cadastrar/usuario', UsuarioCreate.as_view(), name='cadastrar-usuario'),

    path('listar/usuarios', UsuarioList.as_view(), name='listar-usuarios'),
]
