from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout 
from .models import Usuario 
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, "home.html")

# Função para cadastro de usuários
def cadastro(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        tipo_usuario = request.POST.get("tipo_usuario")

        if not email or not password or not tipo_usuario:
            return render(request, "usuarios/cadastro.html")

        if Usuario.objects.filter(email=email).exists():
            return render(request, "usuarios/cadastro.html")


        password2 = request.POST.get("password2")
        if password != password2:
             return render(request, "usuarios/cadastro.html")

        else:
            user = Usuario.objects.create_user(email=email, password=password, tipo_usuario=tipo_usuario)
            return redirect("login")
    return render(request, "usuarios/cadastro.html")

# Função para dashboard da empresa
@login_required
def dashboard_empresa(request):
    if request.user.tipo_usuario != "empresa":
        return redirect("dashboard_candidato")
    return render(request, "usuarios/dashboard_empresa.html")

# Função para dashboard do candidato
@login_required
def dashboard_candidato(request):
    return render(request, "usuarios/dashboard_candidato.html")

# Função para login de usuários
def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, username=email, password=password)

        if user is not None and user.is_active:
            login(request, user)

            if user.tipo_usuario == "empresa":
                return redirect("dashboard_empresa")
            else:
                return redirect("dashboard_candidato")

        else:
            return render(request, "usuarios/login.html", {"error": "Credenciais inválidas."})  

    return render(request, "usuarios/login.html")

# Função para logout de usuários
def logout_view(request):
    logout(request)
    return redirect("login")  