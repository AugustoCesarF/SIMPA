# SIMPA — Entrega 2: Arquitetura de Produção, Backend Django e APIs REST

> **Projeto:** SIMPA (Sistema Inteligente de Monitoramento e Predição Acadêmica)  
> **Instituição:** UniEVANGÉLICA — Centro Universitário de Anápolis  
> **Curso:** Inteligência Artificial / Engenharia de Software  
> **Líder do Projeto:** Augusto César F.  
> **Stack:** Python 3.12+ | Django 5.2 | Django REST Framework | PostgreSQL | HTML5/CSS3 (Glassmorphism Dark UI)  
> **Arquitetura:** MVT (Model-View-Template) com Camada de Serviços e REST APIs  

---

## 🎯 Objetivo da Entrega 2

A **Entrega 2** consolida a migração e evolução do SIMPA, superando a prova de conceito inicial em Flask (Entrega 1) e estabelecendo uma **arquitetura de nível de produção** baseada em **Django 5.2 + Django REST Framework** conectado ao banco de dados relacional **PostgreSQL**, com:

1. **Persistência Relacional Robusta:** Modelagem de domínio com integridade referencial (Estudantes, Turmas, Locais de Aula, Registros Acadêmicos, Comunidade e Logs).
2. **APIs RESTful Completas:** Endpoints CRUD padronizados com validações de entrada estritas (CPF algorítmico, unicidade de RA e códigos).
3. **Segurança e Conformidade (RNF01):** Autenticação via Token, isolamento de segredos em variáveis de ambiente (`.env`), boas práticas da LGPD.
4. **Motor de Indicadores & Predição de Risco (RF09 / Analytics):** Estatística descritiva (média, mediana, desvio padrão, correlação de Pearson) e cálculo heurístico de risco acadêmico com alertas preventivos de evasão.
5. **Interface Visual HUD Escura (Dark Glassmorphism):** Dashboard executivo moderno com métricas em tempo real, navegação fluida e gráficos interativos com Chart.js.

---

## 🏗️ Estrutura do Projeto (Padrão MVT Django)

```
Entrega2/
├── manage.py                   ← Utilitário de comandos Django na raiz
├── requirements.txt            ← Dependências do projeto
├── .env.example                ← Modelo de variáveis de ambiente
├── .env                        ← Variáveis locais de banco de dados (não versionado)
│
├── config/                     ← Configurações centrais do Django
│   ├── settings.py             ← INSTALLED_APPS, DATABASES (PostgreSQL), MIDDLEWARE
│   ├── urls.py                 ← Roteamento mestre MVT e REST APIs
│   ├── asgi.py / wsgi.py       ← Gateways de execução assíncrona/síncrona
│
├── estudantes/                 ← App: Cadastro e Gestão de Estudantes (RF01)
│   ├── models.py               ← Estudante (Nome, RA único, CPF validado, contato, status)
│   ├── serializers.py          ← Validação estrita de CPF da Receita Federal
│   ├── views.py                ← ViewSet REST e operações
│   └── urls.py                 ← Rotas `/api/estudantes/`
│
├── turmas/                     ← App: Gestão de Turmas e Alocação de Salas (RF02, IE04)
│   ├── models.py               ← Turma e LocalAula (campus, bloco, sala, capacidade)
│   ├── serializers.py          ← Validação de códigos e relacionamentos
│   ├── views.py                ← Gestão de turmas e matrículas
│   └── urls.py                 ← Rotas `/api/turmas/`
│
├── registros/                  ← App: Registros Acadêmicos e Painel Principal (RF03-RF09)
│   ├── models.py               ← RegistroAcademico (notas N1, N2, N3, faltas, situação)
│   ├── views.py                ← Dashboard geral MVT e indicadores
│   ├── urls.py                 ← Rotas `/` (HUD) e `/api/registros/`
│   └── templates/registros/    ← Interface do Dashboard Geral
│
├── analytics/                  ← 📊 App: Módulo Analítico e Estatística Descritiva
│   ├── services.py             ← Funções puras: média, mediana, desvio padrão, Pearson, risco
│   ├── views.py                ← Visualizações analíticas e APIs de inteligência
│   └── templates/analytics/    ← Gráficos interativos com Chart.js
│
├── comunidade/                 ← 💬 App: Vida Acadêmica e Integrações (IE01-IE04)
│   ├── models.py               ← PerfilUsuario, TopicoDuvida, RespostaDuvida, LogWhatsApp
│   ├── services.py             ← Integração Meta Cloud API (WhatsApp)
│   └── templates/comunidade/   ← Telas de Perfil, Fórum de Dúvidas e Locais de Aula
│
├── docs/                       ← Documentação da Entrega 2 e Roteiros
│   ├── Apresentacao_Entrega2_Roteiro.md ← Roteiro completo slide a slide para a banca
│   └── Apresentacao_Entrega2.html       ← Slide deck interativo para projeção
│
└── templates/                  ← Templates globais compartilhados (HUD, login, painel)
```

---

## 🚀 Como Executar o Projeto

### 1. Pré-requisitos
- Python 3.12 ou superior instalado
- PostgreSQL rodando localmente (banco `simpa`)
- Dependências instaladas:
```bash
pip install -r requirements.txt
```

### 2. Configuração do `.env`
Crie ou verifique o arquivo `.env` na raiz de `Entrega2/`:
```env
SECRET_KEY=sua-chave-secreta
DB_NAME=simpa
DB_USER=postgres
DB_PASSWORD=sua-senha-postgres
DB_HOST=localhost
DB_PORT=5432
```

### 3. Aplicar Migrações
```bash
python manage.py migrate
```

### 4. Iniciar o Servidor
```bash
python manage.py runserver
```

Acesse no navegador:
- 🎛️ **Dashboard Geral (HUD Escuro):** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- 📊 **Módulo Analítico & Gráficos:** [http://127.0.0.1:8000/analytics/](http://127.0.0.1:8000/analytics/)
- 🏫 **Locais de Aula & WhatsApp:** [http://127.0.0.1:8000/comunidade/locais/](http://127.0.0.1:8000/comunidade/locais/)
- 💬 **Fórum de Dúvidas:** [http://127.0.0.1:8000/comunidade/duvidas/](http://127.0.0.1:8000/comunidade/duvidas/)
- 👤 **Perfil do Usuário:** [http://127.0.0.1:8000/comunidade/perfil/](http://127.0.0.1:8000/comunidade/perfil/)
- 🔐 **Painel Administrativo:** [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## 📊 Matriz de Requisitos Atendidos na Entrega 2

| Código | Requisito | Status | Implementação |
|---|---|:---:|---|
| **RF01** | Cadastro e Gestão de Estudantes | ✅ | `estudantes/` (CRUD, RA único, CPF validado com algoritmo oficial) |
| **RF02** | Gestão de Turmas e Disciplinas | ✅ | `turmas/` (Carga horária, N:N com alunos, alocação de sala) |
| **RF03** | Registro de Notas e Frequência | ✅ | `registros/` (Notas N1, N2, N3, faltas, situação automática) |
| **RF04** | Estatísticas Descritivas Básicas | ✅ | `analytics/services.py` (Média, mediana, desvio padrão, percentis) |
| **RF05** | Indicadores de Desempenho por Turma | ✅ | `analytics/views.py` (Taxas de aprovação, médias comparadas) |
| **RF06** | Relatórios Consolidados | ✅ | `analytics/relatorio/` e exportação estruturada |
| **RF07** | Validação Estrita de Notas (0-10) | ✅ | Serializers e constraints no banco de dados |
| **RF08** | Autenticação e Perfis | ✅ | Django Auth + DRF Token Authentication |
| **RF09** | Predição Heurística de Risco Acadêmico | ✅ | Score ponderado (0-100), faixas Baixo/Médio/Alto e recomendações |
| **RNF01** | Segurança e LGPD | ✅ | Proteção de dados, validação de entradas, .env isolado |
| **RNF02** | Organização Modular de Código | ✅ | Arquitetura MVT desacoplada (models, services, views, serializers) |
| **RNF03** | Qualidade de Dados | ✅ | Tratamento de valores nulos e validação rigorosa de campos |
| **RNF04** | Documentação e UML | ✅ | Diagramas de classes, casos de uso, documentação de rotas e apresentação |
| **IE01** | Avatar e Perfil do Usuário | ✅ | `comunidade/perfil/` com persistência de dados |
| **IE02** | Fórum de Dúvidas Aluno-Professor | ✅ | `comunidade/duvidas/` com resolução de tópicos |
| **IE03** | Integração WhatsApp | ✅ | `comunidade/services.py` (Meta Cloud API / links de grupos) |
| **IE04** | Localização de Aulas | ✅ | `comunidade/locais/` com mapa de bloco, sala e campus |

---

## 👥 Equipe do Projeto
- **Augusto César F.** — Líder do Projeto / Engenharia de Backend & Arquitetura
- **Marcel** — Engenharia de Dados & Backend
- **Nicolas** — Design de Interface (UI/UX) & Frontend HUD
- **Eduardo** — Garantia de Qualidade & Testes
- **Gabriel** — Regras de Negócio & Documentação
