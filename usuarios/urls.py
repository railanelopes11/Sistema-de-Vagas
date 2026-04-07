from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


# Lista de URLs do app "usuarios"
urlpatterns = [
    path("", views.home, name="home"),
    path ("cadastro/", views.cadastro, name="cadastro"),
    path("login/", views.login_view, name="login"),
    path ("logout/", views.logout_view, name="logout"), 
    path ("dashboard_empresa/", views.dashboard_empresa, name="dashboard_empresa"),
    path ("dashboard_candidato/", views.dashboard_candidato, name="dashboard_candidato"),
]
