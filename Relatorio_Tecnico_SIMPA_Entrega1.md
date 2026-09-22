# Relatório Técnico de Desenvolvimento – SIMPA
**Sistema Inteligente de Monitoramento e Predição Acadêmica**
**Fase:** Ciclo 1 / Marco 1 (Semanas 1 a 7)
**Autor/Líder Técnico:** Augusto

---

## 1. Objetivo do Documento
Este relatório detalha tecnicamente todas as implementações, decisões arquiteturais e módulos desenvolvidos para a **Entrega 1 (Marco 1)** do projeto SIMPA. O foco desta etapa foi a construção da base arquitetural, modelagem do sistema, implementação de estruturação orientada a objetos e validação de uma API básica funcional.

---

## 2. Arquitetura do Sistema
O sistema foi desenhado visando escalabilidade e separação de responsabilidades. Para o protótipo inicial, adotou-se a seguinte stack tecnológica:
* **Backend de API e Roteamento:** Desenvolvido em **Python (Flask)**, atuando como o servidor central que responde a requisições REST e serve as páginas estáticas. (O planejamento futuro migrará a lógica central para *Django/Django REST Framework*).
* **Camada de Integração (Scraper):** Módulo autônomo em Python (`requests` e `BeautifulSoup4`) encarregado de acessar o Moodle.
* **Frontend:** Implementado puramente em **HTML5, CSS3 e JavaScript (Vanilla)** para garantir máxima performance sem dependência de bibliotecas externas (como React ou Angular), atendendo restrições de arquitetura.
* **Persistência de Dados (Mock):** Dados simulados em memória para validação das rotas e do algoritmo de IA, em preparação para a entrada do **MySQL** no Ciclo 2.

---

## 3. Modelagem e Orientação a Objetos (POO)
Atendendo aos requisitos da Semana 3 e 4, o sistema foi estruturado seguindo os princípios de Orientação a Objetos.

### 3.1. Entidades de Domínio (`models.py`)
Foram mapeadas e programadas as classes fundamentais do negócio:
* **`Usuario` (Superclasse):** Contém `id`, `nome`, `email`, `senha_hash` e métodos de autenticação.
* **`Aluno` (Subclasse de Usuario):** Adiciona o `RA (matrícula)` e agrega uma lista de seus registros acadêmicos.
* **`Professor` (Subclasse de Usuario):** Adiciona o `departamento` e agrega a lista de turmas lecionadas.
* **`Disciplina` e `Turma`:** Mapeiam a relação de oferta de aulas, vinculando professores, alunos, carga horária e códigos de disciplina.
* **`RegistroAcademico`:** Classe transacional que une um Aluno a uma Turma, contendo `nota1`, `nota2`, `nota3`, `faltas` e métodos internos para calcular média final e situação (Aprovado/Reprovado).
* **`IndicadorRisco`:** Classe analítica que recebe o Aluno e gera a pontuação, motivos e nível de risco.

### 3.2. Diagramas UML
* **Casos de Uso:** Mapeia a interação do Administrador (Coordenador) gerindo alunos, turmas e visualizando riscos, e a integração sistêmica com o AVA (Moodle).
* **Diagrama de Classes:** Espelha a estrutura do código Python, utilizando herança (`Aluno` extends `Usuario`) e composição.

---

## 4. Desenvolvimento da API REST
O arquivo `main.py` fornece uma API básica e completamente funcional que alimenta os dashboards em tempo real:
* **`GET /api/health`:** Rota de verificação de disponibilidade do servidor (Health Check).
* **`GET /api/demo/alunos` e `/disciplinas` e `/matriculas`:** Rotas que fornecem os arrays JSON para popular o Frontend dinamicamente via requisições assíncronas (AJAX/Fetch).
* **`GET /api/demo/kpis`:** Rota de inteligência agregada que processa todos os alunos e retorna totais (Média Geral, Aprovados, Reprovados).
* **`GET /api/demo/risco/<id>`:** Endpoint que aciona o motor de risco de um aluno específico.
* **`POST /api/ava/dados`:** Rota de proxy para comunicação autenticada com o Moodle.

---

## 5. Motor Analítico de Risco (Heurística V1)
Para demonstrar o potencial preditivo do sistema antes da implementação dos modelos de *Machine Learning (Scikit-Learn)*, foi desenvolvido um **Motor Heurístico**.
A lógica da função `_calcular_risco(aluno_id)` funciona da seguinte forma:
1. **Coleta:** Varre todos os registros acadêmicos do aluno.
2. **Avaliação de Média:** Penaliza o score em +40 pontos se a média for < 5.0, ou +20 pontos se for < 6.5.
3. **Avaliação de Faltas:** Penaliza +30 pontos para excesso crítico (>10) ou +15 pontos para alerta (>5).
4. **Histórico de Situação:** Aplica pesagem cumulativa por reprovações ativas e recuperações.
5. **Classificação Final:** Converte o *Score* (limitado a 100) para Nível de Risco:
   * 0 a 25%: **BAIXO**
   * 26% a 55%: **MÉDIO**
   * Acima de 55%: **ALTO**
6. **Geração de Ações:** O algoritmo produz listas de *Motivos* (ex: "Média baixa em Engenharia") e *Recomendações Pedagógicas* automatizadas.

---

## 6. Integração com o AVA (Web Scraping)
O módulo `moodle_scraper.py` resolveu o desafio técnico de extração de dados do sistema da instituição:
* **Bypass de Segurança (CSRF):** O script não faz apenas um POST simples. Ele primeiro acessa a página de login, realiza um *parsing* HTML usando BeautifulSoup para extrair o campo oculto `logintoken`, e só então injeta a senha e o RA, imitando um navegador real.
* **Gerenciamento de Sessão:** Utiliza `requests.Session()` para reter os cookies de autenticação de MoodleSession.
* **Extração Direcionada:** Navega silenciosamente pelas rotas `/my/` (Meus Cursos) e `/grade/report/overview/index.php` (Notas do Usuário), extraindo as tabelas para dicionários JSON.
* **Performance:** Foi implementado no Backend um **Cache em memória com TTL (Time-To-Live) de 15 minutos**. Se o mesmo aluno logar duas vezes, o SIMPA não faz nova requisição ao Moodle, garantindo velocidade no login e evitando punições no IP (Rate Limit).

---

## 7. Interfaces de Usuário (Frontend SPA)
O sistema adotou um padrão *Single Page Application* na experiência, gerenciando abas sem recarregar a página. Duas visões principais foram criadas:

### 7.1. Dashboard Administrativo (`dashboard.html`)
Desenvolvido para coordenação, contém:
* **Painel de Indicadores:** Resumo gerencial.
* **Gestão de Alunos:** Tabela com botões que simulam operações CRUD (Adicionar, Editar, Excluir) e atualizam indicadores em tempo real.
* **Gestão de Disciplinas:** Relação de matérias.
* **Painel de Análise de Risco:** Exibe os *Risk Cards* ordenados automaticamente do aluno com maior risco para o menor.
* **Relatórios:** Tabelas analíticas geradas pelo Javascript calculando Taxa de Aprovação, Desempenho por Disciplina e Ranking de Melhores Alunos (Top 6).

### 7.2. Painel do Aluno (`painel_aluno.html`)
Visão restrita e personalizada:
* **Meu Painel:** Resumo rápido da situação (quantas matérias cursando, saúde das notas).
* **Minhas Notas:** Boletim individual.
* **Meu Risco:** Transparência para o próprio aluno visualizar onde o SIMPA detecta pontos de alerta e ler as recomendações geradas.
* **Dados do AVA:** Aba crua que exibe a exata importação do Moodle (Cursos e Notas originais).

---

## 8. Métricas da Sprint (Marco 1)
* **Tempo de Desenvolvimento Estimado:** 15 a 18 horas
* **Volume de Código:** 1.361 linhas escritas do zero
* **Artefatos Gerados:**
  * `app/main.py` (Backend API & Rotas)
  * `app/moodle_scraper.py` (Módulo Integrador)
  * `app/models.py` (Mapeamento de Entidades POO)
  * `app/templates/login.html` (UI Autenticação)
  * `app/templates/dashboard.html` (UI Administrativa)
  * `app/templates/painel_aluno.html` (UI Estudante)
  * Documentação Estrutural (Modelagem, UML, README, Changelog)
