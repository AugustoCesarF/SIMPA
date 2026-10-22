import statistics
from decimal import Decimal
from django.db.models import Avg, Count, Q
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets, filters, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from estudantes.models import Estudante
from turmas.models import Turma
from .models import RegistroAcademico
from .serializers import RegistroAcademicoSerializer


# ---------------------------------------------------------------------------
# ViewSet Principal da API REST (RF07)
# ---------------------------------------------------------------------------
class RegistroAcademicoViewSet(viewsets.ModelViewSet):
    """
    CRUD de Registros Acadêmicos (Notas e Frequência) — RF03 e RF07.
    """
    queryset = RegistroAcademico.objects.select_related("estudante", "turma").all().order_by("-atualizado_em")
    serializer_class = RegistroAcademicoSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["estudante__nome", "estudante__matricula", "turma__nome", "turma__codigo", "periodo"]
    ordering_fields = ["nota", "frequencia", "atualizado_em", "periodo"]

    def get_queryset(self):
        qs = super().get_queryset()
        estudante_id = self.request.query_params.get("estudante_id")
        turma_id = self.request.query_params.get("turma_id")
        periodo = self.request.query_params.get("periodo")

        if estudante_id:
            qs = qs.filter(estudante_id=estudante_id)
        if turma_id:
            qs = qs.filter(turma_id=turma_id)
        if periodo:
            qs = qs.filter(periodo=periodo)
        return qs


# ---------------------------------------------------------------------------
# RF04 / RF05 / RF07 — Endpoint de Indicadores e Estatística Descritiva
# ---------------------------------------------------------------------------
@api_view(["GET"])
@permission_classes([AllowAny])
def api_indicadores(request):
    """
    RF04/RF05/RF07 — Estatística descritiva e indicadores acadêmicos.
    Calcula média, mediana, desvio-padrão, mínimos, máximos e taxas de aprovação.
    Pode filtrar por ?turma_id=<id> e ?periodo=<periodo>.
    """
    turma_id = request.query_params.get("turma_id")
    periodo = request.query_params.get("periodo")

    qs = RegistroAcademico.objects.all()
    if turma_id:
        qs = qs.filter(turma_id=turma_id)
    if periodo:
        qs = qs.filter(periodo=periodo)

    total_registros = qs.count()

    if total_registros > 0:
        notas = [float(r.nota) for r in qs]
        frequencias = [float(r.frequencia) for r in qs]

        media_notas = round(statistics.mean(notas), 2)
        mediana_notas = round(statistics.median(notas), 2)
        desvio_padrao_notas = round(statistics.stdev(notas), 2) if len(notas) > 1 else 0.0
        nota_minima = min(notas)
        nota_maxima = max(notas)

        media_freq = round(statistics.mean(frequencias), 1)

        aprovados = sum(1 for r in qs if float(r.nota) >= 6.0 and float(r.frequencia) >= 75.0)
        recuperacao = sum(1 for r in qs if 4.0 <= float(r.nota) < 6.0 and float(r.frequencia) >= 75.0)
        reprovados_falta = sum(1 for r in qs if float(r.frequencia) < 75.0)
        reprovados_nota = sum(1 for r in qs if float(r.nota) < 4.0 and float(r.frequencia) >= 75.0)
        total_reprovados = reprovados_falta + reprovados_nota

        taxa_aprovacao = round((aprovados / total_registros) * 100, 1)

        total_estudantes = Estudante.objects.filter(ativo=True).count()
        total_turmas = Turma.objects.filter(ativa=True).count()

        return Response({
            "total_alunos": total_estudantes,
            "total_turmas": total_turmas,
            "total_registros": total_registros,
            "estatisticas_notas": {
                "media": media_notas,
                "mediana": mediana_notas,
                "desvio_padrao": desvio_padrao_notas,
                "minimo": nota_minima,
                "maximo": nota_maxima,
            },
            "estatisticas_frequencia": {
                "media_percentual": media_freq,
            },
            "situacao": {
                "aprovados": aprovados,
                "recuperacao": recuperacao,
                "reprovados": total_reprovados,
                "reprovados_por_falta": reprovados_falta,
                "reprovados_por_nota": reprovados_nota,
                "taxa_aprovacao_percentual": taxa_aprovacao,
            },
        }, status=status.HTTP_200_OK)

    # Fallback para dados de demonstração se banco estiver vazio
    medias_demo = [m["media"] for m in DEMO_MATRICULAS]
    aprov_demo = sum(1 for m in DEMO_MATRICULAS if m["situacao"] == "Aprovado")
    rep_demo = sum(1 for m in DEMO_MATRICULAS if m["situacao"] in ("Reprovado", "Recuperação"))
    media_geral = round(statistics.mean(medias_demo), 2) if medias_demo else 0.0
    mediana_demo = round(statistics.median(medias_demo), 2) if medias_demo else 0.0
    stdev_demo = round(statistics.stdev(medias_demo), 2) if len(medias_demo) > 1 else 0.0

    return Response({
        "total_alunos": len(DEMO_ALUNOS),
        "total_turmas": len(DEMO_DISCIPLINAS),
        "total_registros": len(DEMO_MATRICULAS),
        "estatisticas_notas": {
            "media": media_geral,
            "mediana": mediana_demo,
            "desvio_padrao": stdev_demo,
            "minimo": min(medias_demo) if medias_demo else 0.0,
            "maximo": max(medias_demo) if medias_demo else 0.0,
        },
        "estatisticas_frequencia": {
            "media_percentual": 88.5,
        },
        "situacao": {
            "aprovados": aprov_demo,
            "recuperacao": sum(1 for m in DEMO_MATRICULAS if m["situacao"] == "Recuperação"),
            "reprovados": rep_demo,
            "taxa_aprovacao_percentual": round((aprov_demo / len(DEMO_MATRICULAS)) * 100, 1) if DEMO_MATRICULAS else 0.0,
        },
    }, status=status.HTTP_200_OK)


# ---------------------------------------------------------------------------
# RF06 / RF07 — Endpoint de Relatórios Consolidados
# ---------------------------------------------------------------------------
@api_view(["GET"])
@permission_classes([AllowAny])
def api_relatorios(request):
    """
    RF06/RF07 — Relatórios consolidados de turmas, alunos e desempenho.
    """
    turmas_qs = Turma.objects.filter(ativa=True).prefetch_related("registros_academicos")
    relatorio_turmas = []

    for t in turmas_qs:
        regs = t.registros_academicos.all()
        if regs.exists():
            notas = [float(r.nota) for r in regs]
            relatorio_turmas.append({
                "turma_id": t.id,
                "codigo": t.codigo,
                "nome": t.nome,
                "professor": t.professor,
                "total_alunos": t.estudantes.count(),
                "media_notas": round(statistics.mean(notas), 2),
                "aprovados": sum(1 for r in regs if float(r.nota) >= 6.0 and float(r.frequencia) >= 75.0),
                "reprovados": sum(1 for r in regs if float(r.nota) < 6.0 or float(r.frequencia) < 75.0),
            })

    # Ranking de estudantes por média
    estudantes_qs = Estudante.objects.filter(ativo=True).prefetch_related("registros_academicos")
    ranking = []
    for est in estudantes_qs:
        regs = est.registros_academicos.all()
        if regs.exists():
            media = round(statistics.mean([float(r.nota) for r in regs]), 2)
            faltas = sum(1 for r in regs if float(r.frequencia) < 75.0)
            ranking.append({
                "aluno_id": est.id,
                "nome": est.nome,
                "matricula": est.matricula,
                "curso": est.curso,
                "media_geral": media,
                "situacao_geral": "Aprovado" if media >= 6.0 and faltas == 0 else "Alerta",
            })
    ranking.sort(key=lambda x: x["media_geral"], reverse=True)

    return Response({
        "turmas": relatorio_turmas,
        "ranking_alunos": ranking[:10],
        "total_turmas_avaliadas": len(relatorio_turmas),
    }, status=status.HTTP_200_OK)


# ---------------------------------------------------------------------------
# RF09 — Predição de Risco Acadêmico
# ---------------------------------------------------------------------------
def _calcular_risco_estudante(estudante):
    regs = estudante.registros_academicos.all()
    if not regs.exists():
        return {
            "aluno": estudante.nome,
            "ra": estudante.matricula,
            "score": 0,
            "nivel": "SEM DADOS",
            "motivos": ["Sem registros acadêmicos cadastrados até o momento."],
            "recomendacoes": ["Cadastrar avaliações e frequência para calcular o risco."],
        }

    notas = [float(r.nota) for r in regs]
    frequencias = [float(r.frequencia) for r in regs]
    media_geral = statistics.mean(notas)
    media_freq = statistics.mean(frequencias)

    reprovacoes = sum(1 for r in regs if float(r.nota) < 4.0 or float(r.frequencia) < 75.0)
    recuperacoes = sum(1 for r in regs if 4.0 <= float(r.nota) < 6.0 and float(r.frequencia) >= 75.0)

    score = 0
    motivos = []
    recomendacoes = []

    if media_geral < 5.0:
        score += 40
        motivos.append(f"Média geral crítica: {media_geral:.1f}")
        recomendacoes.append("Agendar reforço acadêmico com tutoria individual")
    elif media_geral < 6.5:
        score += 20
        motivos.append(f"Média geral abaixo da meta: {media_geral:.1f}")
        recomendacoes.append("Participar de grupos de estudo e monitorias")

    if media_freq < 75.0:
        score += 35
        motivos.append(f"Frequência abaixo do mínimo regimental (75%): {media_freq:.1f}%")
        recomendacoes.append("Entrar em contato com a coordenação para justificar faltas")
    elif media_freq < 85.0:
        score += 15
        motivos.append(f"Frequência em nível de atenção: {media_freq:.1f}%")

    if reprovacoes > 0:
        score += 25 * reprovacoes
        motivos.append(f"Reprovação em {reprovacoes} disciplina(s)")
        recomendacoes.append("Considerar reoferta com acompanhamento pedagógico")

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
        "aluno": estudante.nome,
        "ra": estudante.matricula,
        "score": score,
        "nivel": nivel,
        "motivos": motivos,
        "recomendacoes": recomendacoes,
    }


@api_view(["GET"])
@permission_classes([AllowAny])
def api_risco_aluno(request, aluno_id):
    """
    RF09 — Análise de Risco de Desempenho Acadêmico de um estudante específico.
    """
    estudante = Estudante.objects.filter(id=aluno_id).prefetch_related("registros_academicos").first()
    if estudante:
        return Response(_calcular_risco_estudante(estudante), status=status.HTTP_200_OK)

    # Fallback para DEMO se não encontrado no DB
    demo = next((a for a in DEMO_ALUNOS if a["id"] == aluno_id), None)
    if demo:
        risco = calcular_risco_demo(aluno_id)
        risco["aluno"] = demo["nome"]
        risco["ra"] = demo["ra"]
        return Response(risco, status=status.HTTP_200_OK)

    return Response({"error": "Estudante não encontrado."}, status=status.HTTP_404_NOT_FOUND)


# ---------------------------------------------------------------------------
# Dashboard Django e Rotas de Compatibilidade
# ---------------------------------------------------------------------------
def dashboard(request):
    resumo = RegistroAcademico.objects.aggregate(
        total=Count("id"),
        media_notas=Avg("nota"),
        media_frequencia=Avg("frequencia"),
    )

    total_estudantes = Estudante.objects.filter(ativo=True).count()
    total_turmas = Turma.objects.filter(ativa=True).count()

    registros_atencao = RegistroAcademico.objects.filter(
        Q(nota__lt=6) | Q(frequencia__lt=75)
    ).select_related("estudante", "turma")

    ultimos_registros = RegistroAcademico.objects.select_related(
        "estudante", "turma"
    ).order_by("-atualizado_em")[:10]

    contexto = {
        "total_estudantes": total_estudantes,
        "total_turmas": total_turmas,
        "total_registros": resumo["total"] or 0,
        "media_notas": resumo["media_notas"],
        "media_frequencia": resumo["media_frequencia"],
        "registros_atencao": registros_atencao[:10],
        "total_atencao": registros_atencao.count(),
        "ultimos_registros": ultimos_registros,
    }

    return render(request, "registros/dashboard.html", contexto)


# ---------------------------------------------------------------------------
# Dados DEMO mantidos para retrocompatibilidade com UI original
# ---------------------------------------------------------------------------
DEMO_ALUNOS = [
    {"id": 1, "nome": "Ana Clara Souza", "ra": "20260001", "email": "ana.souza@aluno.edu.br", "turma": "IA 2º Período - Turma A"},
    {"id": 2, "nome": "Bruno Henrique Lima", "ra": "20260002", "email": "bruno.lima@aluno.edu.br", "turma": "IA 2º Período - Turma A"},
    {"id": 3, "nome": "Carla Rodrigues", "ra": "20260003", "email": "carla.rod@aluno.edu.br", "turma": "IA 2º Período - Turma A"},
    {"id": 4, "nome": "Daniel Ferreira Costa", "ra": "20260004", "email": "daniel.costa@aluno.edu.br", "turma": "IA 2º Período - Turma B"},
    {"id": 5, "nome": "Elena Martins", "ra": "20260005", "email": "elena.mart@aluno.edu.br", "turma": "IA 2º Período - Turma B"},
    {"id": 6, "nome": "Felipe Augusto Ramos", "ra": "20260006", "email": "felipe.ramos@aluno.edu.br", "turma": "IA 2º Período - Turma B"},
]

DEMO_DISCIPLINAS = [
    {"id": 1, "nome": "Engenharia de Software", "codigo": "ES201", "carga_horaria": 80, "professor": "Prof. Ricardo Alves"},
    {"id": 2, "nome": "Banco de Dados", "codigo": "BD201", "carga_horaria": 80, "professor": "Prof. Márcia Tavares"},
    {"id": 3, "nome": "Inteligência Artificial", "codigo": "IA201", "carga_horaria": 60, "professor": "Prof. Carlos Mendes"},
    {"id": 4, "nome": "Matemática Discreta", "codigo": "MD201", "carga_horaria": 60, "professor": "Prof. Juliana Rocha"},
    {"id": 5, "nome": "Projeto Integrador", "codigo": "PI201", "carga_horaria": 40, "professor": "Prof. Eduardo Santos"},
]

DEMO_MATRICULAS = [
    {"aluno_id": 1, "aluno": "Ana Clara Souza", "disciplina": "Engenharia de Software", "n1": 8.5, "n2": 7.0, "n3": 9.0, "faltas": 2, "media": 8.2, "situacao": "Aprovado"},
    {"aluno_id": 1, "aluno": "Ana Clara Souza", "disciplina": "Banco de Dados", "n1": 6.0, "n2": 5.5, "n3": 7.0, "faltas": 5, "media": 6.2, "situacao": "Aprovado"},
    {"aluno_id": 2, "aluno": "Bruno Henrique Lima", "disciplina": "Engenharia de Software", "n1": 4.0, "n2": 3.5, "n3": 5.0, "faltas": 12, "media": 4.2, "situacao": "Reprovado"},
    {"aluno_id": 2, "aluno": "Bruno Henrique Lima", "disciplina": "Inteligência Artificial", "n1": 5.0, "n2": 4.5, "n3": 6.0, "faltas": 8, "media": 5.2, "situacao": "Recuperação"},
    {"aluno_id": 3, "aluno": "Carla Rodrigues", "disciplina": "Matemática Discreta", "n1": 9.0, "n2": 8.5, "n3": 9.5, "faltas": 1, "media": 9.0, "situacao": "Aprovado"},
    {"aluno_id": 3, "aluno": "Carla Rodrigues", "disciplina": "Projeto Integrador", "n1": 7.5, "n2": 8.0, "n3": 8.5, "faltas": 0, "media": 8.0, "situacao": "Aprovado"},
    {"aluno_id": 4, "aluno": "Daniel Ferreira Costa", "disciplina": "Banco de Dados", "n1": 3.0, "n2": 2.5, "n3": 4.0, "faltas": 15, "media": 3.2, "situacao": "Reprovado"},
    {"aluno_id": 4, "aluno": "Daniel Ferreira Costa", "disciplina": "Engenharia de Software", "n1": 5.5, "n2": 6.0, "n3": 4.5, "faltas": 10, "media": 5.3, "situacao": "Recuperação"},
    {"aluno_id": 5, "aluno": "Elena Martins", "disciplina": "Inteligência Artificial", "n1": 7.0, "n2": 7.5, "n3": 8.0, "faltas": 3, "media": 7.5, "situacao": "Aprovado"},
    {"aluno_id": 5, "aluno": "Elena Martins", "disciplina": "Matemática Discreta", "n1": 6.5, "n2": 7.0, "n3": 6.0, "faltas": 4, "media": 6.5, "situacao": "Aprovado"},
    {"aluno_id": 6, "aluno": "Felipe Augusto Ramos", "disciplina": "Projeto Integrador", "n1": 8.0, "n2": 9.0, "n3": 8.5, "faltas": 1, "media": 8.5, "situacao": "Aprovado"},
    {"aluno_id": 6, "aluno": "Felipe Augusto Ramos", "disciplina": "Banco de Dados", "n1": 7.0, "n2": 6.5, "n3": 7.5, "faltas": 3, "media": 7.0, "situacao": "Aprovado"},
]

def demo_alunos(request):
    return JsonResponse(DEMO_ALUNOS, safe=False)

def demo_disciplinas(request):
    return JsonResponse(DEMO_DISCIPLINAS, safe=False)

def demo_matriculas(request):
    return JsonResponse(DEMO_MATRICULAS, safe=False)

def demo_kpis(request):
    medias = [m["media"] for m in DEMO_MATRICULAS]
    aprovados = sum(1 for m in DEMO_MATRICULAS if m["situacao"] == "Aprovado")
    reprovados = sum(1 for m in DEMO_MATRICULAS if m["situacao"] in ("Reprovado", "Recuperação"))
    return JsonResponse({
        "total_alunos": len(DEMO_ALUNOS),
        "media_geral": round(sum(medias) / len(medias), 1) if medias else 0,
        "aprovados": aprovados,
        "reprovados_recuperacao": reprovados,
    })

def calcular_risco_demo(aluno_id):
    matriculas = [m for m in DEMO_MATRICULAS if m["aluno_id"] == aluno_id]
    if not matriculas:
        return {"nivel": "SEM DADOS", "score": 0, "motivos": [], "recomendacoes": []}

    media_geral = sum(m["media"] for m in matriculas) / len(matriculas)
    total_faltas = sum(m["faltas"] for m in matriculas)
    reprovacoes = sum(1 for m in matriculas if m["situacao"] == "Reprovado")
    recuperacoes = sum(1 for m in matriculas if m["situacao"] == "Recuperação")

    score = 0
    motivos = []
    recomendacoes = []

    if media_geral < 5.0:
        score += 40
        motivos.append(f"Média geral muito baixa: {media_geral:.1f}")
        recomendacoes.append("Agendar reforço acadêmico com tutoria individual")
    elif media_geral < 6.5:
        score += 20
        motivos.append(f"Média geral abaixo do ideal: {media_geral:.1f}")
        recomendacoes.append("Participar de grupos de estudo e monitorias")

    if total_faltas > 10:
        score += 30
        motivos.append(f"Excesso de faltas acumuladas: {total_faltas}")
        recomendacoes.append("Verificar questões de saúde ou transporte com a coordenação")
    elif total_faltas > 5:
        score += 15
        motivos.append(f"Faltas acima da média: {total_faltas}")

    if reprovacoes > 0:
        score += 20 * reprovacoes
        motivos.append(f"Reprovação em {reprovacoes} disciplina(s)")
        recomendacoes.append("Considerar cursá-las novamente com acompanhamento")

    if recuperacoes > 0:
        score += 10 * recuperacoes
        motivos.append(f"Em recuperação em {recuperacoes} disciplina(s)")
        recomendacoes.append("Focar nas avaliações de recuperação com revisão dirigida")

    for matricula in matriculas:
        if matricula["media"] < 5.0:
            motivos.append(f"Média muito baixa em {matricula['disciplina']}: {matricula['media']}")

    score = min(score, 100)
    if score <= 25:
        nivel = "BAIXO"
    elif score <= 55:
        nivel = "MÉDIO"
    else:
        nivel = "ALTO"

    if not recomendacoes:
        recomendacoes.append("Manter o bom desempenho e buscar atividades extracurriculares")

    return {"nivel": nivel, "score": score, "motivos": motivos, "recomendacoes": recomendacoes}

def demo_risco(request, aluno_id):
    aluno = next((a for a in DEMO_ALUNOS if a["id"] == aluno_id), None)
    if not aluno:
        return JsonResponse({"error": "Aluno não encontrado"}, status=404)
    risco = calcular_risco_demo(aluno_id)
    risco["aluno"] = aluno["nome"]
    risco["ra"] = aluno["ra"]
    return JsonResponse(risco)
