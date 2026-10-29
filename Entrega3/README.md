# SIMPA — Entrega 3: Módulo Analítico e Inteligência Aplicada

> **Status:** 🟡 Semana 13  
> **Framework:** Django 5.2 + Django REST Framework  
> **Arquitetura:** MVT (Model-View-Template)

---

## 🏗️ Estrutura do Projeto (Padrão MVT Django)

```
Entrega3/
├── manage.py                  ← Utilitário de comandos Django
├── requirements.txt           ← Dependências Python
├── .env.example               ← Modelo de variáveis de ambiente
│
├── config/                    ← Configuração central do projeto
│   ├── settings.py            ← INSTALLED_APPS, DATABASES, etc.
│   └── urls.py                ← Roteamento principal
│
├── estudantes/                ← App: Cadastro de Estudantes
│   ├── models.py              ← M — Model (Estudante)
│   ├── views.py               ← V — View (ViewSet REST)
│   ├── urls.py                ← Roteamento do app
│   └── templates/estudantes/  ← T — Templates HTML
│
├── turmas/                    ← App: Cadastro de Turmas
│   ├── models.py              ← M — Model (Turma)
│   ├── views.py               ← V — View (ViewSet REST)
│   ├── urls.py                ← Roteamento do app
│   └── templates/turmas/      ← T — Templates HTML
│
├── registros/                 ← App: Registros Acadêmicos
│   ├── models.py              ← M — Model (RegistroAcademico)
│   ├── views.py               ← V — Views (dashboard + APIs)
│   ├── urls.py                ← Roteamento do app
│   └── templates/registros/   ← T — Templates HTML
│
└── analytics/                 ← 🆕 App: Módulo Analítico (Entrega 3)
    ├── models.py              ← M — Model (SnapshotEstatistico)
    ├── services.py            ← Lógica estatística pura
    ├── views.py               ← V — Dashboard + APIs JSON
    ├── urls.py                ← Roteamento do app
    └── templates/analytics/   ← T — Templates com Chart.js
        ├── dashboard.html     ← Dashboard analítico
        └── relatorio.html     ← Relatório por período
```

---

## 🔄 Fluxo MVT no SIMPA

```
Requisição HTTP
      ↓
  urls.py          ← Roteador: direciona para a View correta
      ↓
  views.py (V)     ← Processa lógica + chama services.py
      ↓
  models.py (M)    ← ORM: lê/escreve no banco de dados
      ↓
  views.py (V)     ← Recebe dados do Model
      ↓
templates/*.html(T)← Renderiza HTML com dados do contexto
      ↓
  Resposta HTML/JSON
```

---

## 📊 Indicadores Estatísticos (analytics/services.py)

| Função | Indicador | Objetivo |
|---|---|---|
| `calcular_media()` | Média aritmética | Tendência central |
| `calcular_mediana()` | Mediana | Centro resistente a outliers |
| `calcular_desvio_padrao()` | Desvio padrão (σ) | Dispersão das notas |
| `calcular_coef_variacao()` | Coef. Variação (CV%) | Homogeneidade da turma |
| `calcular_percentil()` | P25, P50, P75 | Quartis / boxplot |
| `calcular_pearson()` | Correlação de Pearson r | Nota × frequência |
| `calcular_tendencia()` | Tendência N1→N2→N3 | Evolução do desempenho |
| `calcular_risco_aluno()` | Score de risco (0–100) | Predição de risco |

---

## 🌐 Endpoints

| Rota | Tipo | Descrição |
|---|---|---|
| `/analytics/` | Template HTML | Dashboard com Chart.js |
| `/analytics/relatorio/` | Template HTML | Relatório por período |
| `/analytics/api/estatisticas/` | JSON | Todos os indicadores |
| `/analytics/api/turma/<id>/` | JSON | Stats por turma |
| `/analytics/api/aluno/<id>/risco/` | JSON | Score de risco |
| `/analytics/api/correlacao/` | JSON | Pearson r geral |

---

## 🚀 Como Rodar

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Configurar variáveis de ambiente
cp .env.example .env
# Editar .env com suas credenciais

# 3. Aplicar migrações
python manage.py migrate

# 4. Iniciar servidor
python manage.py runserver
```

Acesse: http://127.0.0.1:8000/analytics/

---

## 🔒 Segurança

- `SECRET_KEY` carregada via `.env` (não versionado)
- `.env` listado no `.gitignore`
- Veja `.env.example` como modelo de configuração
