"""
Views — Módulo Analítico (SIMPA Entrega 3)
Padrão MVT do Django:
  M → registros.RegistroAcademico, turmas.Turma, estudantes.Estudante
  V → estas views (controller no Django)
  T → templates/analytics/*.html
"""

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_GET

from estudantes.models import Estudante
from registros.models import RegistroAcademico
from turmas.models import Turma

from . import services


# -------------------------------------------------------------------------
# VIEW PRINCIPAL — Dashboard Analítico (Template HTML + Chart.js)
# -------------------------------------------------------------------------

@require_GET
def dashboard_analitico(request):
    """
    View principal do módulo analítico.
    Calcula todos os indicadores e passa ao template para renderização
    dos gráficos com Chart.js (visualizações no navegador).
    """
    registros = RegistroAcademico.objects.select_related("estudante", "turma").all()
    stats = services.calcular_estatisticas_gerais(registros)

    # Dados para gráficos (serializados para JSON inline no template)
    import json

    histograma_labels = [h["faixa"] for h in stats["histograma"]]
    histograma_dados = [h["quantidade"] for h in stats["histograma"]]

    # Dados por turma (para gráfico de barras comparativo)
    turmas = Turma.objects.filter(ativa=True)
    turmas_labels = []
    turmas_medias = []
    turmas_aprovacao = []

    for turma in turmas:
        regs = registros.filter(turma=turma)
        if regs.exists():
            s = services.calcular_estatisticas_gerais(regs)
            turmas_labels.append(turma.codigo)
            turmas_medias.append(s["media_notas"])
            turmas_aprovacao.append(s["taxa_aprovacao"])

    # Scatter plot: nota × frequência
    scatter_dados = list(
        registros.values("nota", "frequencia", "estudante__nome")
    )
    scatter_json = json.dumps([
        {"x": float(d["frequencia"]), "y": float(d["nota"]), "label": d["estudante__nome"]}
        for d in scatter_dados
        if d["nota"] is not None and d["frequencia"] is not None
    ])

    contexto = {
        # Indicadores gerais
        "stats": stats,

        # Contagens gerais
        "total_estudantes": Estudante.objects.filter(ativo=True).count(),
        "total_turmas": turmas.count(),
        "total_registros": registros.count(),

        # Dados JSON para Chart.js
        "histograma_labels_json": json.dumps(histograma_labels),
        "histograma_dados_json": json.dumps(histograma_dados),
        "turmas_labels_json": json.dumps(turmas_labels),
        "turmas_medias_json": json.dumps(turmas_medias),
        "turmas_aprovacao_json": json.dumps(turmas_aprovacao),
        "scatter_json": scatter_json,

        # Interpretação textual
        "interpretacoes": stats["interpretacao"]["mensagens"],
    }

    return render(request, "analytics/dashboard.html", contexto)


# -------------------------------------------------------------------------
# API JSON — Estatísticas Gerais
# -------------------------------------------------------------------------

@require_GET
def api_estatisticas_gerais(request):
    """
    Endpoint JSON com todos os indicadores estatísticos gerais.
    GET /analytics/api/estatisticas/
    """
    registros = RegistroAcademico.objects.select_related("estudante", "turma").all()
    stats = services.calcular_estatisticas_gerais(registros)

    # Remove histograma e interpretação (verbosos; há endpoint específico)
    stats.pop("histograma", None)
    stats.pop("interpretacao", None)

    return JsonResponse({"status": "ok", "indicadores": stats})


# -------------------------------------------------------------------------
# API JSON — Estatísticas por Turma
# -------------------------------------------------------------------------

@require_GET
def api_estatisticas_turma(request, turma_id):
    """
    Indicadores estatísticos de uma turma específica.
    GET /analytics/api/turma/<id>/
    """
    turma = get_object_or_404(Turma, pk=turma_id)
    registros = RegistroAcademico.objects.filter(turma=turma).select_related("estudante")
    stats = services.calcular_estatisticas_gerais(registros)
    stats.pop("histograma", None)

    return JsonResponse({
        "status": "ok",
        "turma": {"id": turma.id, "codigo": turma.codigo, "nome": turma.nome},
        "indicadores": stats,
        "interpretacao": stats.get("interpretacao", {}).get("mensagens", []),
    })


# -------------------------------------------------------------------------
# API JSON — Score de Risco Individual
# -------------------------------------------------------------------------

@require_GET
def api_risco_aluno(request, aluno_id):
    """
    Score de risco de evasão/reprovação para um aluno.
    GET /analytics/api/aluno/<id>/risco/
    """
    aluno = get_object_or_404(Estudante, pk=aluno_id)
    registros = RegistroAcademico.objects.filter(estudante=aluno).select_related("turma")
    risco = services.calcular_risco_aluno(registros)

    return JsonResponse({
        "status": "ok",
        "aluno": {"id": aluno.id, "nome": aluno.nome, "matricula": aluno.matricula},
        "risco": risco,
    })


# -------------------------------------------------------------------------
# API JSON — Correlação Nota × Frequência
# -------------------------------------------------------------------------

@require_GET
def api_correlacao(request):
    """
    Coeficiente de Pearson entre nota e frequência de todos os registros.
    GET /analytics/api/correlacao/
    """
    dados = list(
        RegistroAcademico.objects.values("nota", "frequencia")
    )
    notas = [float(d["nota"]) for d in dados if d["nota"] is not None]
    frequencias = [float(d["frequencia"]) for d in dados if d["frequencia"] is not None]

    r = services.calcular_pearson(notas, frequencias)

    if r > 0.7:
        interpretacao = "Correlação forte positiva — frequência influencia significativamente a nota."
    elif r > 0.3:
        interpretacao = "Correlação moderada — frequência tem influência parcial na nota."
    elif r > 0:
        interpretacao = "Correlação fraca positiva — pouca relação entre frequência e nota."
    else:
        interpretacao = "Correlação negativa ou nula — frequência não explica a variação das notas neste conjunto."

    return JsonResponse({
        "status": "ok",
        "pearson_r": r,
        "total_registros": len(notas),
        "interpretacao": interpretacao,
    })


# -------------------------------------------------------------------------
# VIEW — Relatório Completo por Período (Template HTML)
# -------------------------------------------------------------------------

@require_GET
def relatorio_periodo(request):
    """
    Relatório analítico completo por período — renderiza template HTML.
    GET /analytics/relatorio/
    """
    import json

    periodo = request.GET.get("periodo", "")
    registros_base = RegistroAcademico.objects.select_related("estudante", "turma")

    if periodo:
        registros_base = registros_base.filter(periodo=periodo)

    # Estatísticas gerais do período
    stats_gerais = services.calcular_estatisticas_gerais(registros_base)

    # Estatísticas por turma
    turmas_dados = []
    for turma in Turma.objects.filter(ativa=True):
        regs = registros_base.filter(turma=turma)
        if regs.exists():
            s = services.calcular_estatisticas_gerais(regs)
            turmas_dados.append({
                "turma": turma,
                "stats": s,
                "interpretacoes": s["interpretacao"]["mensagens"],
            })

    # Lista de períodos disponíveis
    periodos = list(
        RegistroAcademico.objects
        .values_list("periodo", flat=True)
        .distinct()
        .order_by("periodo")
    )

    # Dados do scatter para o relatório
    scatter_dados = list(registros_base.values("nota", "frequencia", "estudante__nome"))
    scatter_json = json.dumps([
        {"x": float(d["frequencia"]), "y": float(d["nota"]), "label": d["estudante__nome"]}
        for d in scatter_dados
        if d["nota"] is not None and d["frequencia"] is not None
    ])

    contexto = {
        "periodo_selecionado": periodo,
        "periodos": periodos,
        "stats_gerais": stats_gerais,
        "turmas_dados": turmas_dados,
        "scatter_json": scatter_json,
        "interpretacoes_gerais": stats_gerais["interpretacao"]["mensagens"],
    }

    return render(request, "analytics/relatorio.html", contexto)
