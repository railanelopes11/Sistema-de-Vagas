from .models import Candidatura

# Dicionário para mapear níveis de escolaridade a valores numéricos
NIVEL_ESCOLARIDADE = {
    'ensino_fundamental': 1,
    'ensino_medio': 2,
    "tecnologo": 3,
    'ensino_superior': 4,
    'pos_mba_mestrado': 5,
    'doutorado': 6,
}


# Conversão de faixa salarial para intervalo numérico
def faixa_para_intervalo(faixa):
    if faixa == "até 1000":
        return 0, 1000
    elif faixa == "de 1000 a 2000":
        return 1000, 2000
    elif faixa == "de 2000 a 3000":
        return 2000, 3000
    elif faixa == "acima de 3000":
        return 3000, 1000000
    return (0, 0)


# Calcular pontuação do candidato com base em salário e escolaridade
def calcular_pontuacao(candidatura, vaga):
    pontos = 0

    try:
        salario = float(candidatura.pretensao_salarial.replace(",", "").strip())
    except:
        salario = 0

    faixa_min, faixa_max = faixa_para_intervalo(vaga.faixa_salarial)

    if faixa_min <= salario <= faixa_max:
        pontos += 1

    nivel_candidato = NIVEL_ESCOLARIDADE.get(candidatura.ultima_escolaridade, 0)
    nivel_vaga = NIVEL_ESCOLARIDADE.get(vaga.escolaridade_minima, 0)

    if nivel_candidato >= nivel_vaga:
        pontos += 1

    return pontos


# Rankear candidatos de uma vaga com base na pontuação calculada
def rankear_candidatos(vaga):
    candidaturas = Candidatura.objects.filter(vaga=vaga)

    ranking = []

    for candidatura in candidaturas:
        pontos = calcular_pontuacao(candidatura, vaga)
        ranking.append({
            "candidatura": candidatura,
            "pontos": pontos
        })

    ranking.sort(key=lambda x: x["pontos"], reverse=True)
    return ranking



# Validar se o salário é válido
def salario_valido(valor):
    try:
        float(valor)
        return True
    except:
        return False