# Entrega 1 – Planejamento e Modelagem Inicial do Sistema (SIMPA)

Este documento centraliza todo o planejamento exigido para a primeira entrega do **Sistema Inteligente de Monitoramento e Predição Acadêmica (SIMPA)**, atualizado conforme a Listagem de Requisitos Oficial do Projeto Integrador.

---

## 1. Modelagem Inicial do Sistema
A arquitetura do SIMPA será baseada em um modelo distribuído, conectando dados de um banco relacional estruturado (MySQL) com dados em tempo real coletados ativamente do ambiente virtual da instituição (AVA). 

**Estrutura de Módulos (Organização do Código RNF02):**
- **Frontend (HTML/CSS/JS):** Responsável pela interface visual, renderização do dashboard, e formulários de autenticação.
- **Backend (Python com Django):** Centraliza as lógicas em pacotes dedicados (`models/`, `services/`, `api/`, `data/`, `docs/`, `tests/`). Utiliza o Django REST Framework para prover os endpoints (RF07).
- **Integração AVA (`services/raspagem`):** Serviço paralelo focado em se comunicar com o AVA institucional (RF13). Faz extração via API ou *Web Scraping* para capturar dados quando a API oficial não possuir a informação.
- **Módulo de Dados e IA (MySQL + Scikit-learn):** O MySQL armazenará toda a estrutura de alunos, turmas, registros e indicadores. A IA (Nível 2) rodará predições de risco e recomendará ações mitigatórias.

## 2. Definição do Fluxo de Dados do Sistema
O fluxo operacional do SIMPA segue o seguinte ciclo:
1. **Coleta e Autenticação (RF08 e RF13):** O usuário faz o acesso seguro. O sistema permite login padrão (e-mail e senha com JWT/Token) ou a sincronização utilizando credenciais que validem a raspagem no AVA.
2. **Sincronização e Extração:** O backend via requisição orquestra os `services/` e, através das bibliotecas `requests` e `BeautifulSoup`, consome os dados de notas e faltas.
3. **Consolidação (RF03 e RF04):** O Django processa a estatística descritiva (Média, Mediana, Desvio-padrão) e salva os fatos acadêmicos normalizados no MySQL.
4. **Análise Preditiva e Recomendações (RF09 e RF10):** Os serviços de IA utilizam variáveis de entrada (notas, frequência, evolução) e executam a regressão/correlação, devolvendo um grau de Risco (Baixo, Médio, Alto) e justificativas (ex: "agendar reforço").
5. **Visualização (RF06):** O Frontend consome a API (`/indicadores`, `/relatorios`) e renderiza histogramas, dispersões e sésries temporais no Dashboard.

> [!WARNING] Segurança e LGPD (RNF01)
> Todas as entradas passarão por validação e sanitização (prevenção a SQLi e XSS). Dados sensíveis como CPF terão acesso restrito. Senhas dos usuários serão armazenadas obrigatoriamente utilizando hash bcrypt, nunca em texto puro.

## 3. Esboço da Interface (Dashboard)
Baseado no layout moderno validado (*SIMPA interface.pdf* e vídeo do painel), a estrutura visual compreende:

### Tela de Autenticação (Login)
- **Componentes:** Campos de "E-mail" e "Senha", Checkbox "Lembre-se de mim".
- **Integração Externa:** Botão destacado inferior **"Entrar com o AVA"**, possibilitando a sincronização com o sistema da UniEVANGÉLICA.

### Dashboard (Painel Principal)
- **Painel de Indicadores (KPIs):** Resumo no topo da tela com métricas operacionais, alimentado pelas Estatísticas Descritivas do backend.
- **Tabelas Relacionais e Gráficos:**
  - *Visão de Cadastros (RF01, RF02):* Listas para manipulação de Alunos e Turmas.
  - *Registros Acadêmicos (RF03):* Detalhamento granular de notas de 0 a 10 e frequência (com cores indicativas).
  - *Visualizações Analíticas (RF06):* Funcionalidade de filtros e exportação (PNG/PDF).
- **Predição e Alertas:** Exibição da classificação de risco para o aluno (com justificativa gráfica) e ação recomendada sugerida pela IA.

## 4. Definição da Arquitetura Tecnológica
A stack tecnológica atende estritamente às restrições do projeto (RNF02):
- **Frontend (Interface):** HTML, CSS e JavaScript nativos para compor o Dashboard (responsabilidade do integrante Nicolas).
- **Backend (Regras e Orquestração):** **Python** com o framework **Django**. As rotas REST serão desenvolvidas utilizando o **Django REST Framework**.
- **Extração Web e Integração:** Bibliotecas `requests` e `BeautifulSoup4` acionadas de forma programática.
- **Banco de Dados:** **MySQL**, garantindo robustez e conformidade para salvar relações de turmas, alunos e registros acadêmicos.
- **Análise de Dados e Inteligência Artificial:** `scikit-learn` acoplado aos `services/` do Django para os cálculos de predição de risco e regressões (Nível 2).

## 5. Roteiro para a Apresentação Oral (Equipe)
*Equipe: Augusto (Líder), Marcel, Davi, Nicolas, Eduardo, Gabriel.*

1. **Apresentação e Escopo (1 min):** 
   - *"Boa noite, somos a equipe SIMPA. Nosso objetivo com este sistema é prover indicadores acadêmicos claros, unindo gestão de turmas com inteligência preditiva para identificar alunos em risco."*
2. **A Nossa Solução e Interface (2 min):** 
   - *"Nossa interface foi construída em HTML/CSS/JS puros e consome uma API robusta. Na entrada, o aluno pode logar ou sincronizar com o AVA. O painel centraliza a visão acadêmica: desde o cadastro de alunos até os gráficos e estatísticas descritivas (médias, medianas, desvios)."*
3. **A Estrutura Tecnológica e Fluxo de Dados (1 min):**
   - *"O coração do SIMPA é um Backend em Python com Django REST Framework. Os dados são armazenados no MySQL. Quando a API institucional não fornece os dados, criamos serviços autônomos que realizam Web Scraping (usando BeautifulSoup) para raspagem segura no Moodle."*
4. **Viés Ético, Predição e Segurança (1 min):**
   - *"Toda essa coleta tem um fim de acolhimento: utilizamos scikit-learn para gerar predições que recomendam ações de suporte ao invés de punições. Garantimos a LGPD mascarando o CPF e protegendo as senhas com hash forte (bcrypt). Nenhuma senha do AVA de alunos é armazenada de forma desprotegida."*
5. **Próximos Passos (1 min):**
   - *"Nosso cronograma agora é concluir a integração entre o front-end e os endpoints do Django, estabelecendo a base sólida para os módulos estatísticos de Nível 2 que virão a seguir."*
