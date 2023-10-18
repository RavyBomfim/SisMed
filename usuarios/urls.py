from django.urls import path
from django.contrib.auth import views as auth_views
from usuarios.views import SenhaUpdate, UsuarioCreate, UsuarioDelete, UsuarioList, UsuarioUpdate

urlpatterns = [
    path('', auth_views.LoginView.as_view(
        template_name='usuarios/login.html'
    ), name='login'),
    path('login/', auth_views.LoginView.as_view(
        template_name='usuarios/login.html'
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        template_name='usuarios/login.html'
    ), name='logout'),

    path('cadastrar/usuario', UsuarioCreate.as_view(), name='cadastrar-usuario'),

    path('editar/usuario/<int:pk>', UsuarioUpdate.as_view(), name='editar-usuario'),

    path('editar/senha/<int:pk>', SenhaUpdate.as_view(), name='editar-senha'),

    path('excluir/usuario/<int:pk>', UsuarioDelete.as_view(), name='excluir-usuario'),

    path('listar/usuarios', UsuarioList.as_view(), name='listar-usuarios'),
]
