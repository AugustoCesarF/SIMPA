
from django.db.models import Avg, Count, Q
from django.shortcuts import render

from estudantes.models import Estudante
from turmas.models import Turma
from .models import RegistroAcademico


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

from rest_framework import viewsets
from .models import RegistroAcademico
from .serializers import RegistroAcademicoSerializer


class RegistroAcademicoViewSet(viewsets.ModelViewSet):
    queryset = RegistroAcademico.objects.select_related(
        "estudante", "turma"
    ).all()
    serializer_class = RegistroAcademicoSerializer


# APIs de demonstração para o dashboard original do SIMPA

from django.http import JsonResponse


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
    matriculas = [
        m for m in DEMO_MATRICULAS
        if m["aluno_id"] == aluno_id
    ]

    if not matriculas:
        return {
            "nivel": "SEM DADOS",
            "score": 0,
            "motivos": [],
            "recomendacoes": [],
        }

    media_geral = sum(m["media"] for m in matriculas) / len(matriculas)
    total_faltas = sum(m["faltas"] for m in matriculas)
    reprovacoes = sum(
        1 for m in matriculas if m["situacao"] == "Reprovado"
    )
    recuperacoes = sum(
        1 for m in matriculas if m["situacao"] == "Recuperação"
    )

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
            motivos.append(
                f"Média muito baixa em {matricula['disciplina']}: "
                f"{matricula['media']}"
            )

    score = min(score, 100)

    if score <= 25:
        nivel = "BAIXO"
    elif score <= 55:
        nivel = "MÉDIO"
    else:
        nivel = "ALTO"

    if not recomendacoes:
        recomendacoes.append(
            "Manter o bom desempenho e buscar atividades extracurriculares"
        )

    return {
        "nivel": nivel,
        "score": score,
        "motivos": motivos,
        "recomendacoes": recomendacoes,
    }


def demo_risco(request, aluno_id):
    aluno = next(
        (a for a in DEMO_ALUNOS if a["id"] == aluno_id),
        None,
    )

    if not aluno:
        return JsonResponse(
            {"error": "Aluno não encontrado"},
            status=404,
        )

    risco = calcular_risco_demo(aluno_id)
    risco["aluno"] = aluno["nome"]
    risco["ra"] = aluno["ra"]

    return JsonResponse(risco)
