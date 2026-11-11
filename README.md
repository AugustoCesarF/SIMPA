# SIMPA — Sistema Inteligente de Monitoramento e Predição Acadêmica

![Status](https://img.shields.io/badge/Status-Entrega%202%20(Conclu%C3%ADda)-brightgreen)
![Python](https://img.shields.io/badge/Python-3.12%2B-blue)
![Django](https://img.shields.io/badge/Backend-Django%205.2-green)
![Frontend](https://img.shields.io/badge/Frontend-Dark%20HUD%20Glassmorphism-orange)
![Banco](https://img.shields.io/badge/Banco-PostgreSQL-blue)
![Licença](https://img.shields.io/badge/Licen%C3%A7a-Acad%C3%AAmica-lightgrey)

> **Projeto Integrador — UniEVANGÉLICA (Centro Universitário de Anápolis)**  
> Combate à evasão no ensino superior por meio de métricas, indicadores descritivos, predição de risco e integração universitária.

---

## 📁 Organização do Repositório

| Pasta | Descrição | Status |
|---|---|:---:|
| [**Entrega2/**](./Entrega2/) | 🚀 **Snapshot Oficial da Entrega 2** — Backend Django 5.2 MVT, DRF, PostgreSQL, Motor de Risco e HUD | 🟢 **Concluída** |
| [↳ Apresentação](./Entrega2/apresentacao/index.html) | 🎤 **Slide Deck Interativo em HTML** (pronto para projeção F11 com cronômetro e notas) | 🟢 Pronto |
| [↳ Roteiro](./Entrega2/docs/Apresentacao_Entrega2_Roteiro.md) | 📄 **Roteiro Slide a Slide** com falas da equipe, live demo e defesa da banca | 🟢 Pronto |
| [**Entrega1/**](./Entrega1/) | 📦 Snapshot congelado da Entrega 1 (Flask + Protótipo) | ✅ Concluída |
| [**Entrega3/**](./Entrega3/) | 📊 Expansão analítica avançada e comunidade | 🟢 Integrada |
| [**SIMPA/**](./SIMPA/) | ⚙️ Código principal unificado com documentação técnica e relatórios | ✅ Atualizado |
| [**_recursos/**](./_recursos/) | 📚 Dataset real, guia didático e materiais de apoio | 📁 Recursos |

---

## 🚀 Como Executar o Projeto (Entrega 2)

```bash
# 1. Acesse o diretório da Entrega 2
cd Entrega2

# 2. Instale as dependências (caso ainda não tenha instalado)
pip install -r requirements.txt

# 3. Certifique-se de que o PostgreSQL está rodando e execute as migrações:
python manage.py migrate

# 4. Inicie o servidor Django:
python manage.py runserver
```

### 🌐 Rotas Principais no Navegador:
- 🎛️ **Dashboard Geral (HUD Escuro):** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- 📊 **Módulo Analítico & Gráficos Chart.js:** [http://127.0.0.1:8000/analytics/](http://127.0.0.1:8000/analytics/)
- 🏫 **Locais de Aula & WhatsApp:** [http://127.0.0.1:8000/comunidade/locais/](http://127.0.0.1:8000/comunidade/locais/)
- 💬 **Fórum de Dúvidas Aluno-Professor:** [http://127.0.0.1:8000/comunidade/duvidas/](http://127.0.0.1:8000/comunidade/duvidas/)
- 👤 **Meu Perfil Acadêmico:** [http://127.0.0.1:8000/comunidade/perfil/](http://127.0.0.1:8000/comunidade/perfil/)
- 🔐 **Painel Administrativo:** [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## 🎤 Apresentação da Entrega 2
Para abrir a apresentação visual oficial no seu navegador:
- Abra o arquivo [`Entrega2/apresentacao/index.html`](./Entrega2/apresentacao/index.html) no Chrome ou Edge.
- Atalhos do apresentador:
  - `→` ou `Espaço`: Avançar slide
  - `←`: Voltar slide
  - `N`: Exibir/Ocultar notas do orador (script de fala)
  - `F11`: Modo tela cheia para projetor
- Consulte o script completo de fala em: [`Entrega2/docs/Apresentacao_Entrega2_Roteiro.md`](./Entrega2/docs/Apresentacao_Entrega2_Roteiro.md).

---

## 👥 Equipe do Projeto

| Membro | Papel | Responsabilidade Principal |
|---|---|---|
| **Augusto César F.** | Líder do Projeto / Backend | Arquitetura MVT, Motor de Risco e Coordenação |
| **Marcel** | Engenheiro de Dados / Backend | Modelagem PostgreSQL, Migrações e REST APIs |
| **Nicolas** | Designer UI/UX / Frontend | Interface Dark HUD, Glassmorphism e Chart.js |
| **Eduardo** | Engenheiro de QA & Testes | Validações de Entrada, Algoritmo de CPF e Segurança |
| **Gabriel** | Analista de Requisitos & Negócio | Regras Pedagógicas, Documentação Técnica e UML |
