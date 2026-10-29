# SIMPA — Entrega 3: Módulo Analítico e Inteligência Aplicada

> **Status:** 🟢 Semana 13  
> **Framework:** Django 5.2 + Django REST Framework  
> **Arquitetura:** MVT (Model-View-Template) com Camada de Serviços

---

## 🏗️ Estrutura do Projeto (Padrão MVT Django)

```
Entrega3/
├── manage.py                   ← Utilitário de comandos Django na raiz
├── requirements.txt            ← Dependências Python
├── .env.example                ← Modelo de variáveis de ambiente
│
├── config/                     ← Configuração central do projeto
│   ├── settings.py             ← INSTALLED_APPS, DATABASES, etc.
│   └── urls.py                 ← Roteamento central MVT e APIs
│
├── estudantes/                 ← App: Cadastro e Gestão de Estudantes
│   ├── models.py               ← M — Model (Estudante: RA, CPF, contato, status)
│   ├── views.py                ← V — View (ViewSet REST)
│   ├── urls.py                 ← Roteamento do app
│   └── admin.py                ← Painel administrativo
│
├── turmas/                     ← App: Gestão de Turmas e Locais de Aula
│   ├── models.py               ← M — Models (Turma, LocalAula: campus, sala, bloco)
│   ├── views.py                ← V — ViewSet REST (matrículas, alocações de sala)
│   ├── urls.py                 ← Roteamento do app
│   └── admin.py                ← Painel administrativo
│
├── registros/                  ← App: Registros Acadêmicos
│   ├── models.py               ← M — Model (RegistroAcademico: notas, frequência)
│   ├── views.py                ← V — Dashboard geral e APIs demo
│   ├── urls.py                 ← Roteamento do app
│   └── templates/registros/    ← T — Template do Dashboard Geral
│
├── analytics/                  ← 📊 Módulo Analítico (Entrega 3)
│   ├── models.py               ← M — Model (SnapshotEstatistico)
│   ├── services.py             ← Camada de Serviços (estatística descritiva pura)
│   ├── views.py                ← V — Views (Dashboard, Relatórios, APIs estatísticas)
│   ├── urls.py                 ← Roteamento do módulo analítico
│   └── templates/analytics/    ← T — Templates com Chart.js
│       ├── dashboard.html      ← Dashboard analítico com 4 gráficos interativos
│       └── relatorio.html      ← Relatório analítico por período/turma
│
└── comunidade/                 ← 💬 Módulo de Comunidade & Vida Universitária
    ├── models.py               ← M — Models (PerfilUsuario, TopicoDuvida, RespostaDuvida, LogWhatsApp)
    ├── services.py             ← Integração Meta WhatsApp Business Cloud API
    ├── views.py                ← V — APIViews + Template Views (MVT)
    ├── urls.py                 ← APIs REST do módulo
    ├── template_urls.py        ← Rotas das páginas HTML
    └── templates/comunidade/   ← T — Templates HTML modernos e responsivos
        ├── perfil.html         ← IE01: Avatar e Perfil do Usuário
        ├── duvidas.html        ← IE02: Sistema de Dúvidas Aluno-Professor
        └── locais.html         ← IE04: Locais de Aula + IE03: Grupos e Alertas WhatsApp
```

---

## 🔄 Fluxo MVT no SIMPA

```
   Navegador / Usuário (HTTP Request)
                 ↓
           config/urls.py (Roteador Central)
                 ↓
           views.py (Controller / View no Django)
                 ↓
       ┌─────────┴─────────┐
       ↓                   ↓
   services.py         models.py (Django ORM)
(Estatística / Meta API)   ↓ (Banco de Dados PostgreSQL)
       ↓                   ↓
       └─────────┬─────────┘
                 ↓
        templates/*.html (Django Template Language + Chart.js)
                 ↓
   Resposta HTTP renderizada no navegador (HTML / CSS / JS)
```

---

## 📋 Funcionalidades Implementadas (Checklist Entrega 3)

### 📊 Módulo Analítico & Estatística Aplicada
- [x] **Média Aritmética e Mediana** (`calcular_media`, `calcular_mediana`)
- [x] **Desvio Padrão ($\sigma$) e Coeficiente de Variação (CV%)** (`calcular_desvio_padrao`, `calcular_coef_variacao`)
- [x] **Percentis e Quartis** ($P_{25}, P_{50}, P_{75}$)
- [x] **Correlação Linear de Pearson ($r$)** entre Nota e Frequência
- [x] **Análise de Tendência** ($N_1 \to N_2 \to N_3$) com detecção de evolução
- [x] **Score Ponderado de Risco Acadêmico (0–100)** com classificação `BAIXO`, `MÉDIO` e `ALTO`
- [x] **Interpretação Textual Automatizada** baseada nos indicadores da turma
- [x] **4 Visualizações Gráficas com Chart.js**:
  - Histograma de distribuição de notas
  - Scatter plot (gráfico de dispersão) de correlação Nota $\times$ Frequência
  - Comparativo de médias por turma com linha de corte
  - Gráfico Donut da taxa de aprovação

### 🌟 Funcionalidades Extras Integradas (IE01 a IE04)
- [x] **IE01 — Avatar e Perfil do Usuário**: Foto de perfil com fallback gerado via `ui-avatars`, biografia, telefone, curso e chave de notificações WhatsApp (`/comunidade/perfil/`).
- [x] **IE02 — Sistema de Comunidade (Dúvidas Aluno-Professor)**: Postagem de dúvidas por turma/disciplina, respostas colaborativas, marcação de solução aceita e filtro de busca (`/comunidade/duvidas/`).
- [x] **IE03 — Integração com WhatsApp (Meta Cloud API)**: Disparo oficial de notificações via Meta WhatsApp Cloud API v19.0, templates homologados, logs de auditoria e links oficiais de grupos de turma (`/comunidade/locais/`).
- [x] **IE04 — Exibição da Localização da Aula**: Mapeamento completo de campus, bloco, sala, andar, capacidade e tipo de espaço por turma (`/comunidade/locais/`).

---

## 🌐 Mapa de Rotas e Telas

| Rota | Tipo | Descrição |
|---|---|---|
| `/` | Template HTML | Dashboard Geral do SIMPA |
| `/analytics/` | Template HTML | Dashboard Analítico com Gráficos Chart.js |
| `/analytics/relatorio/` | Template HTML | Relatório Analítico filtrado por período e turma |
| `/comunidade/perfil/` | Template HTML | **IE01** — Tela de Perfil e Avatar |
| `/comunidade/duvidas/` | Template HTML | **IE02** — Feed de Dúvidas da Comunidade |
| `/comunidade/locais/` | Template HTML | **IE04 + IE03** — Locais de Aula e Grupos WhatsApp |
| `/admin/` | Admin Django | Painel de controle completo de todos os modelos |
| `/analytics/api/estatisticas/` | JSON API | Indicadores estatísticos descritivos gerais |
| `/analytics/api/turma/<id>/` | JSON API | Indicadores estatísticos da turma |
| `/analytics/api/aluno/<id>/risco/` | JSON API | Score de risco individual de evasão/reprovação |
| `/analytics/api/correlacao/` | JSON API | Coeficiente $r$ de Pearson geral |
| `/api/comunidade/topicos/` | JSON API | CRUD de dúvidas da comunidade |
| `/api/comunidade/whatsapp/` | JSON API | Auditoria e disparo de WhatsApp Meta Cloud |

---

## ❓ O que é requests + BeautifulSoup4 no SIMPA?

No SIMPA, as bibliotecas **`requests`** e **`BeautifulSoup4`** estão presentes no módulo de integração com o AVA/Moodle (`moodle_scraper.py`):
- **`requests`**: Biblioteca padrão da indústria para requisições HTTP (faz login seguro, autenticação por cookies e download das páginas HTML do Moodle).
- **`BeautifulSoup4`**: Biblioteca de *web scraping* e *parsing* HTML (percorre as tabelas do portal acadêmico e extrai automaticamente notas $N_1, N_2, N_3$, faltas e frequências dos alunos).
- **Objetivo no SIMPA**: Eliminar o trabalho manual de digitação de notas por parte do professor, sincronizando dados diretamente do Moodle da instituição para o banco de dados do SIMPA.

---

## 🚀 Como Executar o Projeto

```bash
# 1. Acesse o diretório da Entrega 3
cd Entrega3

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Configure as variáveis de ambiente (.env)
cp .env.example .env

# 4. Aplique as migrações no banco
python manage.py migrate

# 5. Inicie o servidor Django
python manage.py runserver
```

Acesse o sistema no navegador:
- **Painel Analítico (E3):** `http://127.0.0.1:8000/analytics/`
- **Locais de Aula (IE04):** `http://127.0.0.1:8000/comunidade/locais/`
- **Comunidade (IE02):** `http://127.0.0.1:8000/comunidade/duvidas/`
- **Perfil do Usuário (IE01):** `http://127.0.0.1:8000/comunidade/perfil/`
