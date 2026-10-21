"""
SIMPA — Sistema Inteligente de Monitoramento e Predição Acadêmica
Backend unificado: serve o frontend (templates/static) e a API de scraping.

Rotas:
    GET  /                    → Tela de login
    GET  /dashboard           → Painel principal
    POST /api/ava/dados       → Scraping autenticado no AVA
    GET  /api/health          → Health check
    GET  /api/demo/alunos     → Dados demo para popular o dashboard
"""

import time, json, os
from flask import Flask, request, jsonify, render_template, send_from_directory

app = Flask(__name__,
            template_folder=os.path.join(os.path.dirname(__file__), "templates"),
            static_folder=os.path.join(os.path.dirname(__file__), "static"))

# ---------------------------------------------------------------------------
# Cache do scraper
# ---------------------------------------------------------------------------
CACHE_TTL_SECONDS = 60 * 15
_cache = {}

# ---------------------------------------------------------------------------
# Dados DEMO (simulam o dataset do guia didático)
# ---------------------------------------------------------------------------
DEMO_ALUNOS = [
    {"id": 1, "nome": "Ana Clara Souza",      "ra": "20260001", "email": "ana.souza@aluno.edu.br",      "turma": "IA 2º Período - Turma A"},
    {"id": 2, "nome": "Bruno Henrique Lima",   "ra": "20260002", "email": "bruno.lima@aluno.edu.br",     "turma": "IA 2º Período - Turma A"},
    {"id": 3, "nome": "Carla Rodrigues",       "ra": "20260003", "email": "carla.rod@aluno.edu.br",      "turma": "IA 2º Período - Turma A"},
    {"id": 4, "nome": "Daniel Ferreira Costa", "ra": "20260004", "email": "daniel.costa@aluno.edu.br",   "turma": "IA 2º Período - Turma B"},
    {"id": 5, "nome": "Elena Martins",         "ra": "20260005", "email": "elena.mart@aluno.edu.br",     "turma": "IA 2º Período - Turma B"},
    {"id": 6, "nome": "Felipe Augusto Ramos",  "ra": "20260006", "email": "felipe.ramos@aluno.edu.br",   "turma": "IA 2º Período - Turma B"},
]

DEMO_DISCIPLINAS = [
    {"id": 1, "nome": "Engenharia de Software",  "codigo": "ES201",  "carga_horaria": 80, "professor": "Prof. Ricardo Alves"},
    {"id": 2, "nome": "Banco de Dados",           "codigo": "BD201",  "carga_horaria": 80, "professor": "Prof. Márcia Tavares"},
    {"id": 3, "nome": "Inteligência Artificial",   "codigo": "IA201",  "carga_horaria": 60, "professor": "Prof. Carlos Mendes"},
    {"id": 4, "nome": "Matemática Discreta",       "codigo": "MD201",  "carga_horaria": 60, "professor": "Prof. Juliana Rocha"},
    {"id": 5, "nome": "Projeto Integrador",        "codigo": "PI201",  "carga_horaria": 40, "professor": "Prof. Eduardo Santos"},
]

DEMO_MATRICULAS = [
    {"aluno_id": 1, "aluno": "Ana Clara Souza",      "disciplina": "Engenharia de Software", "n1": 8.5, "n2": 7.0, "n3": 9.0, "faltas": 2,  "media": 8.2,  "situacao": "Aprovado"},
    {"aluno_id": 1, "aluno": "Ana Clara Souza",      "disciplina": "Banco de Dados",          "n1": 6.0, "n2": 5.5, "n3": 7.0, "faltas": 5,  "media": 6.2,  "situacao": "Aprovado"},
    {"aluno_id": 2, "aluno": "Bruno Henrique Lima",   "disciplina": "Engenharia de Software", "n1": 4.0, "n2": 3.5, "n3": 5.0, "faltas": 12, "media": 4.2,  "situacao": "Reprovado"},
    {"aluno_id": 2, "aluno": "Bruno Henrique Lima",   "disciplina": "Inteligência Artificial","n1": 5.0, "n2": 4.5, "n3": 6.0, "faltas": 8,  "media": 5.2,  "situacao": "Recuperação"},
    {"aluno_id": 3, "aluno": "Carla Rodrigues",       "disciplina": "Matemática Discreta",    "n1": 9.0, "n2": 8.5, "n3": 9.5, "faltas": 1,  "media": 9.0,  "situacao": "Aprovado"},
    {"aluno_id": 3, "aluno": "Carla Rodrigues",       "disciplina": "Projeto Integrador",     "n1": 7.5, "n2": 8.0, "n3": 8.5, "faltas": 0,  "media": 8.0,  "situacao": "Aprovado"},
    {"aluno_id": 4, "aluno": "Daniel Ferreira Costa", "disciplina": "Banco de Dados",          "n1": 3.0, "n2": 2.5, "n3": 4.0, "faltas": 15, "media": 3.2,  "situacao": "Reprovado"},
    {"aluno_id": 4, "aluno": "Daniel Ferreira Costa", "disciplina": "Engenharia de Software", "n1": 5.5, "n2": 6.0, "n3": 4.5, "faltas": 10, "media": 5.3,  "situacao": "Recuperação"},
    {"aluno_id": 5, "aluno": "Elena Martins",         "disciplina": "Inteligência Artificial","n1": 7.0, "n2": 7.5, "n3": 8.0, "faltas": 3,  "media": 7.5,  "situacao": "Aprovado"},
    {"aluno_id": 5, "aluno": "Elena Martins",         "disciplina": "Matemática Discreta",    "n1": 6.5, "n2": 7.0, "n3": 6.0, "faltas": 4,  "media": 6.5,  "situacao": "Aprovado"},
    {"aluno_id": 6, "aluno": "Felipe Augusto Ramos",  "disciplina": "Projeto Integrador",     "n1": 8.0, "n2": 9.0, "n3": 8.5, "faltas": 1,  "media": 8.5,  "situacao": "Aprovado"},
    {"aluno_id": 6, "aluno": "Felipe Augusto Ramos",  "disciplina": "Banco de Dados",          "n1": 7.0, "n2": 6.5, "n3": 7.5, "faltas": 3,  "media": 7.0,  "situacao": "Aprovado"},
]

def _calcular_risco(aluno_id):
    """Heurística simples de Score de Risco baseada em médias e faltas."""
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

    # Motivos específicos por disciplina
    for m in matriculas:
        if m["media"] < 5.0:
            motivos.append(f"Média muito baixa em {m['disciplina']}: {m['media']}")

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


# ---------------------------------------------------------------------------
# Rotas — Frontend
# ---------------------------------------------------------------------------
@app.route("/")
def login_page():
    return render_template("login.html")

@app.route("/dashboard")
def dashboard_page():
    return render_template("dashboard.html")

# ---------------------------------------------------------------------------
# Rotas — API
# ---------------------------------------------------------------------------
@app.route("/api/health")
def health():
    return jsonify({"status": "ok"})

@app.route("/api/demo/alunos")
def demo_alunos():
    return jsonify(DEMO_ALUNOS)

@app.route("/api/demo/disciplinas")
def demo_disciplinas():
    return jsonify(DEMO_DISCIPLINAS)

@app.route("/api/demo/matriculas")
def demo_matriculas():
    return jsonify(DEMO_MATRICULAS)

@app.route("/api/demo/kpis")
def demo_kpis():
    total = len(DEMO_ALUNOS)
    medias = [m["media"] for m in DEMO_MATRICULAS]
    media_geral = sum(medias) / len(medias) if medias else 0
    aprovados = sum(1 for m in DEMO_MATRICULAS if m["situacao"] == "Aprovado")
    reprovados = sum(1 for m in DEMO_MATRICULAS if m["situacao"] in ("Reprovado", "Recuperação"))
    return jsonify({
        "total_alunos": total,
        "media_geral": round(media_geral, 1),
        "aprovados": aprovados,
        "reprovados_recuperacao": reprovados,
    })

@app.route("/api/demo/risco/<int:aluno_id>")
def demo_risco(aluno_id):
    aluno = next((a for a in DEMO_ALUNOS if a["id"] == aluno_id), None)
    if not aluno:
        return jsonify({"error": "Aluno não encontrado"}), 404
    risco = _calcular_risco(aluno_id)
    risco["aluno"] = aluno["nome"]
    risco["ra"] = aluno["ra"]
    return jsonify(risco)

@app.route("/api/ava/dados", methods=["POST"])
def get_dados_ava():
    try:
        from moodle_scraper import MoodleAuthError, fetch_all_data
    except ImportError:
        return jsonify({"error": "Módulo moodle_scraper não encontrado"}), 500

    creds = request.get_json()
    if not creds or "username" not in creds or "password" not in creds:
        return jsonify({"error": "username e password obrigatórios"}), 400

    try:
        now = time.time()
        cached = _cache.get(creds["username"])
        if cached and (now - cached["timestamp"] < CACHE_TTL_SECONDS):
            data = cached["data"]
        else:
            data = fetch_all_data(creds["username"], creds["password"])
            _cache[creds["username"]] = {"data": data, "timestamp": now}
    except Exception as e:
        return jsonify({"error": str(e)}), 502

    return jsonify({"fonte": "AVA UniEVANGÉLICA", "cache_ttl_segundos": CACHE_TTL_SECONDS, **data})


if __name__ == "__main__":
    print()
    print("=" * 60)
    print("  SIMPA — Sistema Inteligente de Monitoramento")
    print("  e Predição Acadêmica")
    print("=" * 60)
    print()
    print("  Acesse no navegador: http://127.0.0.1:8000")
    print()
    print("=" * 60)
    app.run(host="127.0.0.1", port=8000, debug=False)
