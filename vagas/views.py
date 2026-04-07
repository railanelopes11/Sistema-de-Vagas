from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models.functions import TruncMonth
from .models import Vaga, Candidatura
from .utils import rankear_candidatos, salario_valido
from django.db.models import Count
from datetime import datetime

#Função para criar uma nova vaga de emprego
@login_required
def criar_vaga(request):
    if request.user.tipo_usuario != "empresa":
        return redirect("dashboard_candidato")
    
    if request.method == "POST":
        nome_vaga = request.POST.get("nome_vaga")
        requisitos = request.POST.get("requisitos")
        faixa_salarial = request.POST.get("faixa_salarial")
        escolaridade_minima = request.POST.get("escolaridade_minima")
        

        Vaga.objects.create(
            nome_vaga=nome_vaga,
            requisitos=requisitos,
            faixa_salarial=faixa_salarial,
            escolaridade_minima=escolaridade_minima,
            empresa=request.user)
        return redirect("dashboard_empresa")

    return render(request, "vagas/criar_vaga.html")

# Função para listar todas as vagas de emprego
def listar_vagas(request):
    vagas = Vaga.objects.annotate(total_candidatos=Count('candidaturas'))
    return render(request, "vagas/lista_vagas.html", {"vagas": vagas})

# Função para exibir detalhes dos candidatos da vaga vaga e o ranking de pontuação
def detalhes_vaga(request, vaga_id):   
    vaga = Vaga.objects.get(id=vaga_id)
    ranking = rankear_candidatos(vaga)
    return render(request, "vagas/detalhes_vaga.html", {"vaga": vaga, "ranking": ranking})

# Função para listar as vagas criadas pela empresa logada
@login_required
def minhas_vagas(request):
    if request.user.tipo_usuario != "empresa":
        return redirect("dashboard_candidato")
    
    vagas = Vaga.objects.filter(empresa=request.user)
    return render(request, "vagas/minhas_vagas.html", {"vagas": vagas})

# Função para editar uma vaga de emprego existente
@login_required
def editar_vaga(request, vaga_id):
    vaga = Vaga.objects.get(id=vaga_id)

    if request.user.tipo_usuario != "empresa":
        return redirect("dashboard_candidato")
    
    if request.method == "POST":
        vaga.nome_vaga = request.POST.get("nome_vaga")
        vaga.requisitos = request.POST.get("requisitos")
        vaga.faixa_salarial = request.POST.get("faixa_salarial")
        vaga.escolaridade_minima = request.POST.get("escolaridade_minima")
        vaga.save()
        return redirect("minhas_vagas")

    return render(request, "vagas/editar_vaga.html", {"vaga": vaga})

# Função para deletar uma vaga de emprego existente
@login_required
def deletar_vaga(request, vaga_id):
    vaga = get_object_or_404(Vaga, id=vaga_id)
   
    if request.user.tipo_usuario != "empresa":
        return redirect("dashboard_candidato")
    
    if request.method == "POST":
        vaga.delete()
        return redirect("minhas_vagas")

    return render(request, "vagas/deletar_vaga.html", {"vaga": vaga})

# Função para o candidato se candidatar a uma vaga de emprego
@login_required
def candidatar(request, vaga_id):
    vaga = get_object_or_404(Vaga, id=vaga_id)

    if request.user.tipo_usuario != "candidato":
        return redirect("dashboard_empresa")

    if request.method == "POST":
        nome_completo = request.POST.get("nome_completo")
        pretensao_salarial = request.POST.get("pretensao_salarial")
        experiencia = request.POST.get("experiencia")
        ultima_escolaridade = request.POST.get("ultima_escolaridade")

        if not nome_completo or not pretensao_salarial or not experiencia or not ultima_escolaridade:
            return redirect(request.path)

        if not salario_valido(pretensao_salarial):
            return redirect(request.path)
                
        if Candidatura.objects.filter(vaga=vaga, candidato=request.user).exists():
            return redirect("listar_vagas")

      
        Candidatura.objects.create(
            vaga=vaga,
            candidato=request.user,
            nome_completo=nome_completo,
            pretensao_salarial=pretensao_salarial,
            experiencia=experiencia,
            ultima_escolaridade=ultima_escolaridade
        )

        return redirect("listar_vagas")

    return render(request, "vagas/candidatar_vaga.html", {"vaga": vaga})

# Função para gerar relatórios de vagas e candidaturas por mês
def relatorios(request):
    vagas = Vaga.objects.all()
    meses_vagas = []
    total_vagas = []

    for month in range(1, 13):
        count = vagas.filter(data_criacao__month=month).count()
        meses_vagas.append(datetime(2026, month, 1).strftime('%b'))  # Ex: Jan, Feb
        total_vagas.append(count)

    candidaturas = Candidatura.objects.all()
    meses_candidatos = []
    total_candidatos = []

    for month in range(1, 13):
        count = candidaturas.filter(vaga__data_criacao__month=month).count()
        meses_candidatos.append(datetime(2026, month, 1).strftime('%b'))
        total_candidatos.append(count)

    context = {
        "meses_vagas": meses_vagas,
        "total_vagas": total_vagas,
        "meses_candidatos": meses_candidatos,
        "total_candidatos": total_candidatos,
    }
    return render(request, "vagas/relatorios.html", context)
