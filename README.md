# SIMPA - Sistema Inteligente de Monitoramento e Predição Acadêmica

![Status](https://img.shields.io/badge/Status-Entrega%201%20(Prot%C3%B3tipo%20Conclu%C3%ADdo)-success)
![Linguagem](https://img.shields.io/badge/Python-3.14-blue)
![Frontend](https://img.shields.io/badge/Frontend-HTML%2FCSS%2FJS-orange)

Projeto Integrador focado no combate à evasão no ensino superior através de métricas, indicadores e Inteligência Artificial. Este repositório contém a **Entrega 1** do sistema, que inclui a modelagem da arquitetura e o protótipo funcional da interface e do motor de coleta de dados.

## 🚀 Funcionalidades Atuais (Entrega 1)

* **Integração com AVA (Moodle):** Raspagem (Web Scraping) autenticada para buscar cursos e notas em tempo real.
* **Dashboard Interativo:** Painel de indicadores (KPIs), listagem de alunos, disciplinas e matrículas com design moderno (Dark Mode).
* **Análise de Risco (Simulação):** Motor heurístico que gera o *Score de Risco* (Baixo, Médio, Alto), listando motivos e recomendações pedagógicas.
* **Gestão de Alunos (Frontend):** Funcionalidades de adicionar, editar e excluir alunos na tabela do dashboard via interatividade JS (Toast Notifications).

## 🛠️ Tecnologias Utilizadas

Conforme a *Listagem de Requisitos*, o projeto final utilizará Django e MySQL. Para esta **Entrega 1 (Protótipo Rápido)**, a stack construída foi:
* **Backend:** Python + Flask (atuando como microserviço para a API e rotas web).
* **Scraping:** `requests` + `BeautifulSoup4`.
* **Frontend:** HTML5, CSS3 e JavaScript (Vanilla), sem dependência de frameworks externos pesados.

## ⚙️ Como executar o projeto localmente

1. Certifique-se de ter o Python instalado.
2. Instale as dependências:
   ```bash
   pip install flask requests beautifulsoup4
   ```
3. Navegue até a pasta `app/` e inicie o servidor:
   ```bash
   cd app
   python main.py
   ```
4. Abra o navegador em: [http://127.0.0.1:8000](http://127.0.0.1:8000)

## 👥 Equipe
* **Augusto** - Líder do Projeto
* **Marcel**
* **Davi**
* **Nicolas**
* **Eduardo**
* **Gabriel**

---
*Documentação oficial, requisitos e guias encontram-se na raiz do repositório (`Entrega1_SIMPA.md`, `Listagem_de_Requisitos_SIMPA.docx`, etc).*
