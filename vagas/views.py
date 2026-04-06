from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Vaga, Candidatura
from django.contrib import messages
from .utils import rankear_candidatos, salario_valido
from django.db.models import Count


def index(request):
    return render(request, "vagas/index.html")  

@login_required
def criar_vaga(request):
    if request.user.tipo_usuario != "empresa":
        return redirect("index")
    
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

def listar_vagas(request):
    vagas = Vaga.objects.annotate(total_candidatos=Count('candidaturas'))
    return render(request, "vagas/lista_vagas.html", {"vagas": vagas})

def detalhes_vaga(request, vaga_id):   
    vaga = Vaga.objects.get(id=vaga_id)
    ranking = rankear_candidatos(vaga)
    return render(request, "vagas/detalhes_vaga.html", {"vaga": vaga, "ranking": ranking})


@login_required
def minhas_vagas(request):
    if request.user.tipo_usuario != "empresa":
        return redirect("index")
    
    vagas = Vaga.objects.filter(empresa=request.user)
    return render(request, "vagas/minhas_vagas.html", {"vagas": vagas})

@login_required
def editar_vaga(request, vaga_id):
    vaga = Vaga.objects.get(id=vaga_id)

    if request.user.tipo_usuario != "empresa":
        return redirect("index")
    
    if request.method == "POST":
        vaga.nome_vaga = request.POST.get("nome_vaga")
        vaga.requisitos = request.POST.get("requisitos")
        vaga.faixa_salarial = request.POST.get("faixa_salarial")
        vaga.escolaridade_minima = request.POST.get("escolaridade_minima")
        vaga.save()
        return redirect("index")

    return render(request, "vagas/editar_vaga.html", {"vaga": vaga})

@login_required
def deletar_vaga(request, vaga_id):
    vaga = get_object_or_404(Vaga, id=vaga_id)
    print(f"Test vaga: {vaga}")
    if request.user.tipo_usuario != "empresa":
        messages.error(request, "Você não tem permissão para deletar esta vaga.")
        return redirect("index")
    
    if request.method == "POST":
        vaga.delete()
        messages.success(request, "Vaga deletada com sucesso!")
        return redirect("minhas_vagas")

    return redirect("minhas_vagas")

@login_required
def candidatar(request, vaga_id):
    vaga = get_object_or_404(Vaga, id=vaga_id)

    if request.user.tipo_usuario != "candidato":
        messages.error(request, "Apenas candidatos podem se candidatar.")
        return redirect("index")

    if request.method == "POST":
        nome_completo = request.POST.get("nome_completo")
        pretensao_salarial = request.POST.get("pretensao_salarial")
        experiencia = request.POST.get("experiencia")
        ultima_escolaridade = request.POST.get("ultima_escolaridade")

        if not nome_completo or not pretensao_salarial or not experiencia or not ultima_escolaridade:
            messages.error(request, "Todos os campos são obrigatórios.")
            return redirect(request.path)

        if not salario_valido(pretensao_salarial):
            messages.error(request, "Pretensão salarial inválida.")
            return redirect(request.path)
                
        if Candidatura.objects.filter(vaga=vaga, candidato=request.user).exists():
            messages.warning(request, "Você já se candidatou a esta vaga.")
            return redirect("listar_vagas")

      
        Candidatura.objects.create(
            vaga=vaga,
            candidato=request.user,
            nome_completo=nome_completo,
            pretensao_salarial=pretensao_salarial,
            experiencia=experiencia,
            ultima_escolaridade=ultima_escolaridade
        )

        messages.success(request, "Candidatura realizada com sucesso!")
        return redirect("listar_vagas")

    return render(request, "vagas/candidatar_vaga.html", {"vaga": vaga})

def relatorio(request):
    vagas = Vaga.objects.all()
    relatorio_vagas = []

    for vaga in vagas:
        numero_candidatos = vaga.candidatura_set.count()
        relatorio_vagas.append({
            "vaga": vaga,
            "numero_candidatos": numero_candidatos
        })

    return render(request, "vagas/relatorio.html", {"relatorio_vagas": relatorio_vagas})

