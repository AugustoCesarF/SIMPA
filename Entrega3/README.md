# SIMPA — Entrega 3: Módulo Analítico e Inteligência Aplicada

> **Status:** 🟡 Em desenvolvimento (Semana 13)  
> **Framework:** Django 5.2 + Django REST Framework  
> **Arquitetura:** MVT (Model-View-Template)

---

## 📐 Arquitetura MVT

```
django_backend/
├── config/                  ← Configuração central (settings, urls)
│   ├── settings.py
│   └── urls.py
│
├── estudantes/              ← App: Gerenciamento de Estudantes
│   ├── models.py            ← M — Model (Estudante)
│   ├── views.py             ← V — View (ViewSet REST)
│   └── templates/           ← T — Templates (admin)
│
├── turmas/                  ← App: Gerenciamento de Turmas
│   ├── models.py            ← M — Model (Turma)
│   ├── views.py             ← V — View (ViewSet REST)
│   └── templates/           ← T — Templates (admin)
│
├── registros/               ← App: Registros Acadêmicos (Entrega 2)
│   ├── models.py            ← M — Model (RegistroAcademico)
│   ├── views.py             ← V — Views (dashboard + APIs demo)
│   └── templates/registros/ ← T — Templates HTML
│
└── analytics/               ← 🆕 App: Módulo Analítico (Entrega 3)
    ├── models.py            ← M — SnapshotEstatistico
    ├── services.py          ← Serviço estatístico (média, σ, Pearson)
    ├── views.py             ← V — Dashboard + APIs JSON
    ├── urls.py              ← Rotas do módulo
    └── templates/analytics/ ← T — Dashboard HTML + Chart.js
        ├── dashboard.html
        └── relatorio.html
```

---

## 📊 Indicadores Estatísticos Implementados

| Indicador | Função | Objetivo |
|---|---|---|
| Média Aritmética | `calcular_media()` | Tendência central |
| Mediana | `calcular_mediana()` | Centro resistente a outliers |
| Desvio Padrão (σ) | `calcular_desvio_padrao()` | Dispersão das notas |
| Coef. de Variação (CV) | `calcular_coef_variacao()` | Homogeneidade da turma |
| Percentis P25, P75 | `calcular_percentil()` | Quartis / boxplot |
| Correlação de Pearson | `calcular_pearson()` | Relação nota × frequência |
| Tendência N1→N2→N3 | `calcular_tendencia()` | Evolução do desempenho |
| Score de Risco | `calcular_risco_aluno()` | Predição heurística (0–100) |

---

## 🌐 Endpoints

| Rota | Tipo | Descrição |
|---|---|---|
| `/analytics/` | Template HTML | Dashboard analítico com Chart.js |
| `/analytics/relatorio/` | Template HTML | Relatório por período/turma |
| `/analytics/api/estatisticas/` | JSON | Todos os indicadores gerais |
| `/analytics/api/turma/<id>/` | JSON | Indicadores de uma turma |
| `/analytics/api/aluno/<id>/risco/` | JSON | Score de risco individual |
| `/analytics/api/correlacao/` | JSON | Pearson nota × frequência |

---

## 🚀 Como Rodar

```bash
cd Entrega3/django_backend

# Instalar dependências
pip install django djangorestframework python-dotenv psycopg2-binary

# Configurar variáveis de ambiente
cp .env.example .env
# Edite o .env com suas credenciais de banco

# Aplicar migrações
python manage.py migrate

# Iniciar servidor
python manage.py runserver
```

Acesse em: http://127.0.0.1:8000/analytics/

---

## 🎨 Visualizações (Chart.js)

- **Histograma** — Distribuição de notas por faixa (0-1, 1-2, ..., 9-10)
- **Scatter Plot** — Correlação visual nota × frequência
- **Barras** — Média por turma com linha de corte (6.0)
- **Donut** — Taxa de aprovação por turma

---

## 🔒 Segurança

A `SECRET_KEY` e credenciais de banco são carregadas via `.env` (não versionado).  
Veja `.env.example` para configuração.
