"""
Services — Módulo Analítico (SIMPA Entrega 3)

Toda a lógica de cálculo estatístico fica aqui (camada de serviço),
separada das Views (seguindo o princípio MVT + Service Layer).

Indicadores implementados:
  - Média aritmética
  - Mediana
  - Desvio padrão populacional
  - Coeficiente de variação (CV)
  - Percentis (P25, P75)
  - Correlação de Pearson (nota × frequência)
  - Tendência entre avaliações (N1 → N2 → N3)
  - Score de risco heurístico (0–100)
"""

import math
from typing import Optional


# ---------------------------------------------------------------------------
# Funções estatísticas puras (sem dependência de Django)
# ---------------------------------------------------------------------------

def calcular_media(valores: list) -> float:
    """Média aritmética simples."""
    if not valores:
        return 0.0
    return round(sum(valores) / len(valores), 2)


def calcular_mediana(valores: list) -> float:
    """Mediana — valor central após ordenação."""
    if not valores:
        return 0.0
    ordenados = sorted(valores)
    n = len(ordenados)
    meio = n // 2
    if n % 2 == 0:
        return round((ordenados[meio - 1] + ordenados[meio]) / 2, 2)
    return round(ordenados[meio], 2)


def calcular_desvio_padrao(valores: list) -> float:
    """Desvio padrão populacional (divide por N)."""
    if len(valores) < 2:
        return 0.0
    media = calcular_media(valores)
    variancia = sum((x - media) ** 2 for x in valores) / len(valores)
    return round(math.sqrt(variancia), 2)


def calcular_coef_variacao(valores: list) -> float:
    """
    Coeficiente de variação (%).
    Mede a dispersão relativa — útil para comparar turmas.
    CV < 15% → turma homogênea
    CV 15-30% → dispersão moderada
    CV > 30% → turma heterogênea
    """
    media = calcular_media(valores)
    if media == 0:
        return 0.0
    dp = calcular_desvio_padrao(valores)
    return round((dp / media) * 100, 2)


def calcular_percentil(valores: list, p: float) -> float:
    """
    Percentil p (0–100) usando interpolação linear.
    Ex.: p=25 → primeiro quartil (Q1)
    """
    if not valores:
        return 0.0
    ordenados = sorted(valores)
    n = len(ordenados)
    indice = (p / 100) * (n - 1)
    inferior = int(indice)
    fracao = indice - inferior
    if inferior + 1 < n:
        return round(ordenados[inferior] + fracao * (ordenados[inferior + 1] - ordenados[inferior]), 2)
    return round(ordenados[inferior], 2)


def calcular_pearson(x: list, y: list) -> float:
    """
    Coeficiente de correlação de Pearson entre dois vetores.
    Retorna valor entre -1 e 1.
      r > 0.7  → correlação forte positiva
      r 0.3–0.7 → correlação moderada
      r < 0.3  → correlação fraca
    """
    n = min(len(x), len(y))
    if n < 2:
        return 0.0

    x = x[:n]
    y = y[:n]
    mx = calcular_media(x)
    my = calcular_media(y)

    numerador = sum((xi - mx) * (yi - my) for xi, yi in zip(x, y))
    denom_x = math.sqrt(sum((xi - mx) ** 2 for xi in x))
    denom_y = math.sqrt(sum((yi - my) ** 2 for yi in y))

    if denom_x == 0 or denom_y == 0:
        return 0.0

    return round(numerador / (denom_x * denom_y), 4)


def calcular_tendencia(sequencia: list) -> dict:
    """
    Analisa a tendência em uma sequência de valores (ex: N1, N2, N3).
    Retorna variações absolutas e classificação de tendência.
    """
    if len(sequencia) < 2:
        return {"variacao_total": 0.0, "tendencia": "ESTAVEL", "variacoes": []}

    variacoes = [
        round(sequencia[i + 1] - sequencia[i], 2)
        for i in range(len(sequencia) - 1)
    ]
    variacao_total = round(sequencia[-1] - sequencia[0], 2)

    if variacao_total > 0.5:
        tendencia = "CRESCENTE"
    elif variacao_total < -0.5:
        tendencia = "DECRESCENTE"
    else:
        tendencia = "ESTAVEL"

    return {
        "variacao_total": variacao_total,
        "tendencia": tendencia,
        "variacoes": variacoes,
    }


# ---------------------------------------------------------------------------
# Funções de análise sobre dados reais (integradas ao Django ORM)
# ---------------------------------------------------------------------------

def calcular_estatisticas_gerais(registros_qs) -> dict:
    """
    Recebe um QuerySet de RegistroAcademico e retorna
    um dicionário completo de indicadores estatísticos.
    """
    dados = list(registros_qs.values("nota", "frequencia", "situacao_original"))

    notas = [float(d["nota"]) for d in dados if d["nota"] is not None]
    frequencias = [float(d["frequencia"]) for d in dados if d["frequencia"] is not None]

    if not notas:
        return _estatisticas_vazias()

    aprovados = sum(1 for d in dados if d.get("situacao_original") == "Aprovado")
    recuperacao = sum(1 for d in dados if d.get("situacao_original") == "Recuperação")
    reprovados = sum(1 for d in dados if d.get("situacao_original") == "Reprovado")
    total = len(dados)

    return {
        # Tendência central
        "media_notas": calcular_media(notas),
        "mediana_notas": calcular_mediana(notas),

        # Dispersão
        "desvio_padrao": calcular_desvio_padrao(notas),
        "coef_variacao": calcular_coef_variacao(notas),
        "nota_minima": round(min(notas), 2),
        "nota_maxima": round(max(notas), 2),

        # Percentis (quartis)
        "percentil_25": calcular_percentil(notas, 25),
        "percentil_50": calcular_percentil(notas, 50),
        "percentil_75": calcular_percentil(notas, 75),

        # Frequência
        "media_frequencia": calcular_media(frequencias),
        "desvio_frequencia": calcular_desvio_padrao(frequencias),

        # Correlação
        "correlacao_nota_frequencia": calcular_pearson(notas, frequencias),

        # Situação
        "total_alunos": total,
        "aprovados": aprovados,
        "recuperacao": recuperacao,
        "reprovados": reprovados,
        "taxa_aprovacao": round(aprovados / total * 100, 1) if total > 0 else 0.0,

        # Histograma (faixas de nota)
        "histograma": _calcular_histograma(notas),

        # Interpretações
        "interpretacao": _interpretar_turma(
            calcular_media(notas),
            calcular_coef_variacao(notas),
            calcular_pearson(notas, frequencias),
        ),
    }


def calcular_risco_aluno(registros_aluno_qs) -> dict:
    """
    Calcula o score de risco individual de um aluno (0–100).
    Retorna nível, score, motivos e recomendações pedagógicas.
    """
    dados = list(registros_aluno_qs.values(
        "nota", "frequencia", "situacao_original", "turma__nome"
    ))

    if not dados:
        return {"nivel": "SEM DADOS", "score": 0, "motivos": [], "recomendacoes": []}

    notas = [float(d["nota"]) for d in dados]
    frequencias = [float(d["frequencia"]) for d in dados]
    media_geral = calcular_media(notas)
    media_freq = calcular_media(frequencias)
    reprovacoes = sum(1 for d in dados if d.get("situacao_original") == "Reprovado")
    recuperacoes = sum(1 for d in dados if d.get("situacao_original") == "Recuperação")

    score = 0
    motivos = []
    recomendacoes = []

    # --- Fator nota ---
    if media_geral < 5.0:
        score += 40
        motivos.append(f"Média geral muito baixa: {media_geral:.1f}")
        recomendacoes.append("Agendar reforço acadêmico com tutoria individual")
    elif media_geral < 6.5:
        score += 20
        motivos.append(f"Média geral abaixo do ideal: {media_geral:.1f}")
        recomendacoes.append("Participar de grupos de estudo e monitorias")

    # --- Fator frequência ---
    if media_freq < 75:
        score += 30
        motivos.append(f"Frequência média crítica: {media_freq:.1f}%")
        recomendacoes.append("Verificar questões de saúde ou transporte com a coordenação")
    elif media_freq < 85:
        score += 15
        motivos.append(f"Frequência abaixo do ideal: {media_freq:.1f}%")
        recomendacoes.append("Melhorar regularidade de presença às aulas")

    # --- Fator reprovações ---
    if reprovacoes > 0:
        score += 20 * reprovacoes
        motivos.append(f"Reprovação em {reprovacoes} disciplina(s)")
        recomendacoes.append("Considerar cursá-las novamente com acompanhamento pedagógico")

    # --- Fator recuperação ---
    if recuperacoes > 0:
        score += 10 * recuperacoes
        motivos.append(f"Em recuperação em {recuperacoes} disciplina(s)")
        recomendacoes.append("Focar nas avaliações de recuperação com revisão dirigida")

    score = min(score, 100)

    if score <= 25:
        nivel = "BAIXO"
    elif score <= 55:
        nivel = "MÉDIO"
    else:
        nivel = "ALTO"

    if not recomendacoes:
        recomendacoes.append("Manter o bom desempenho e buscar atividades extracurriculares")

    return {
        "nivel": nivel,
        "score": score,
        "motivos": motivos,
        "recomendacoes": recomendacoes,
        "media_notas": media_geral,
        "media_frequencia": media_freq,
    }


# ---------------------------------------------------------------------------
# Funções auxiliares internas
# ---------------------------------------------------------------------------

def _calcular_histograma(notas: list) -> list:
    """Agrupa notas em faixas de 1 ponto (0-1, 1-2, ..., 9-10)."""
    faixas = [
        {"faixa": f"{i}-{i+1}", "min": i, "max": i + 1, "quantidade": 0}
        for i in range(0, 10)
    ]
    for nota in notas:
        idx = min(int(nota), 9)
        faixas[idx]["quantidade"] += 1
    return faixas


def _interpretar_turma(media: float, cv: float, pearson: float) -> dict:
    """Gera texto interpretativo automático dos indicadores."""
    msgs = []

    # Interpretação da média
    if media >= 8.0:
        msgs.append("✅ Turma com excelente desempenho médio.")
    elif media >= 6.0:
        msgs.append("⚠️ Turma com desempenho satisfatório, mas com espaço para melhoria.")
    else:
        msgs.append("🚨 Turma com desempenho médio abaixo do mínimo esperado.")

    # Interpretação do CV
    if cv < 15:
        msgs.append("Turma homogênea (CV < 15%) — alunos com desempenho similar.")
    elif cv < 30:
        msgs.append("Dispersão moderada (CV 15–30%) — há diferenças significativas entre os alunos.")
    else:
        msgs.append("Turma heterogênea (CV > 30%) — forte variação entre os alunos.")

    # Interpretação da correlação
    if pearson > 0.7:
        msgs.append("Forte correlação entre frequência e nota (r={:.2f}) — presença impacta diretamente o desempenho.".format(pearson))
    elif pearson > 0.3:
        msgs.append("Correlação moderada frequência × nota (r={:.2f}).".format(pearson))
    else:
        msgs.append("Correlação fraca frequência × nota (r={:.2f}) — outros fatores influenciam o desempenho.".format(pearson))

    return {"mensagens": msgs}


def _estatisticas_vazias() -> dict:
    """Retorna estrutura vazia quando não há dados."""
    return {
        "media_notas": 0.0, "mediana_notas": 0.0,
        "desvio_padrao": 0.0, "coef_variacao": 0.0,
        "nota_minima": 0.0, "nota_maxima": 0.0,
        "percentil_25": 0.0, "percentil_50": 0.0, "percentil_75": 0.0,
        "media_frequencia": 0.0, "desvio_frequencia": 0.0,
        "correlacao_nota_frequencia": 0.0,
        "total_alunos": 0, "aprovados": 0, "recuperacao": 0, "reprovados": 0,
        "taxa_aprovacao": 0.0,
        "histograma": _calcular_histograma([]),
        "interpretacao": {"mensagens": ["Sem dados disponíveis para análise."]},
    }
