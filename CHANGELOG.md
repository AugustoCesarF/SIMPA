# Registro de Alterações (Changelog) - Entrega 1

**Documentado por:** Augusto (Líder do Projeto)  
**Objetivo:** Preparação para o primeiro commit no GitHub (Fechamento da Sprint / Entrega 1).

## 📊 Métricas de Desenvolvimento desta Entrega
- **Tempo Estimado de Desenvolvimento:** ~15 a 18 horas (incluindo modelagem de arquitetura, design da interface, construção do web scraper e integração do protótipo no Flask).
- **Total de Linhas de Código Escritas/Modificadas (Diretório `app/`):** **1.361 linhas**.
- **Total de Arquivos Criados/Refatorados no Código:** 4 arquivos chave (+ arquivos de documentação).

## 📝 Comentários Técnicos e Alterações (por Augusto)

### 1. Backend Unificado (`app/main.py`)
- **Linhas:** 178 linhas | **Tamanho:** 10 KB
- **O que mudou/foi acrescentado:**
  - Migração da prova de conceito original de FastAPI/Pydantic para **Flask** nativo. Isso eliminou gargalos de compilação em C++ (devido ao Pydantic no Windows) e tornou o setup da equipe 100% "plug and play".
  - Criação de todas as rotas da API (`/api/demo/kpis`, `/api/demo/alunos`, etc.) para simular a conexão que teremos no banco MySQL futuro.
  - Integração do endpoint `/api/ava/dados` com a mecânica de cache (TTL de 15 min) para evitar bans do Moodle.
  - Algoritmo heurístico provisório inserido diretamente no backend para calcular o "Score de Risco" (que futuramente será movido para Scikit-Learn/IA).

### 2. Microserviço de Raspagem (`app/moodle_scraper.py`)
- **Linhas:** 117 linhas | **Tamanho:** 5 KB
- **O que mudou/foi acrescentado:**
  - Implementação robusta de Web Scraping utilizando `BeautifulSoup`.
  - Mecânica de extração do `logintoken` para contornar a segurança anti-CSRF do portal.
  - Navegação automatizada pelos endpoints `/my/` (Cursos) e `/grade/report/overview/index.php` (Visão Geral de Notas).

### 3. Tela de Autenticação (`app/templates/login.html`)
- **Linhas:** 414 linhas | **Tamanho:** 15 KB
- **O que mudou/foi acrescentado:**
  - Design construído do zero usando HTML e CSS nativo (sem dependência de frameworks, atendendo restrição do front-end).
  - Implementação do layout escuro com "partículas" flutuantes em CSS puro para um visual imersivo e moderno.
  - Adição do Modal de Conexão com o AVA. O formulário não dá reload na página: ele faz um *fetch* assíncrono pro Flask, exibe um *loading spinner* e trata os erros (Ex: credenciais inválidas) com exibição na tela via JavaScript.

### 4. Dashboard Principal (`app/templates/dashboard.html`)
- **Linhas:** 652 linhas | **Tamanho:** 36 KB
- **O que mudou/foi acrescentado:**
  - Construção da interface com layout em grid (Painéis, Sidebar, Topbar).
  - **Sistema de Toast Notifications:** Criado via JavaScript para dar feedback em tempo real para o usuário ("Módulo em desenvolvimento", "Aluno excluído", etc.).
  - **CRUD Frontend Simulado:** Botões de "+ Novo Aluno", "Editar" e "Excluir" operam ativamente sobre o DOM (modais funcionais preenchem os dados na tabela e ajustam a contagem de KPIs no topo da tela).
  - **Modal de Análise de Risco:** Layout robusto contendo um medidor visual de Score (círculo com cores dinâmicas verde/amarelo/vermelho), recebendo os "Motivos" e "Recomendações" dinamicamente direto da API Flask.

## 🚀 Próximos Passos (Próxima Sprint)
- Transportar a lógica do `main.py` (Flask) para a estrutura final em **Django** e **Django REST Framework** (conforme RNF02).
- Levantar o banco MySQL e substituir as rotas de `demo` pela importação real dos 15 CSVs do Guia Didático do Dataset.
