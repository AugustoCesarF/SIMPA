# SIMPA — Sistema Inteligente de Monitoramento e Predição Acadêmica

![Status](https://img.shields.io/badge/Status-Entrega%202%20(Em%20Produção)-blue)
![Python](https://img.shields.io/badge/Python-3.14-blue)
![Django](https://img.shields.io/badge/Backend-Django%205.2-green)
![Frontend](https://img.shields.io/badge/Frontend-HTML%2FCSS%2FJS-orange)
![Licença](https://img.shields.io/badge/Licença-Acadêmica-lightgrey)

> Projeto Integrador — Combate à evasão no ensino superior por meio de métricas, indicadores e Inteligência Artificial.

---

## 📁 Organização do Repositório

Este repositório segue uma estrutura de pastas por entrega, com o código de desenvolvimento sempre atualizado na pasta SIMPA/.

| Pasta | Descrição |
|---|---|
| [SIMPA/](./SIMPA/) | ✅ Código principal — **sempre atualizado** (trabalhe aqui) |
| [Entrega1/](./Entrega1/) | 📦 Snapshot congelado da Entrega 1 (Flask + Protótipo) |
| [Entrega2/](./Entrega2/) | 🚧 Em produção — Django REST Framework + MySQL |
| [Entrega3/](./Entrega3/) | 🔜 A iniciar na próxima sprint |
| [EntregaFinal/](./EntregaFinal/) | 🏁 Build final consolidado |
| [_recursos/](./_recursos/) | 📚 Dataset, guia didático e materiais de apoio |

---

## 🚀 Como executar (Entrega 2 — Backend Django)

`ash
# 1. Ative o ambiente virtual
.venv\Scripts\activate

# 2. Instale as dependências
pip install -r SIMPA/app/requirements.txt

# 3. Configure o ambiente
copy SIMPA\django_backend\.env.example SIMPA\django_backend\.env
# Edite o .env com suas credenciais do banco

# 4. Rode as migrações
cd SIMPA/django_backend
python manage.py migrate

# 5. Inicie o servidor
python manage.py runserver
`

Acesse: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🛠️ Stack Tecnológica

| Camada | Tecnologia |
|---|---|
| Frontend | HTML5, CSS3, JavaScript (Vanilla) |
| Backend | Python 3.14 + Django 5.2 + Django REST Framework |
| Banco de Dados | MySQL (produção) / PostgreSQL (desenvolvimento) |
| Scraping AVA | equests + BeautifulSoup4 |
| IA / Predição | scikit-learn (Entrega 3) |

---

## 👥 Equipe

| Membro | Papel |
|---|---|
| **Augusto** | Líder do Projeto / Backend |
| **Marcel** | Desenvolvimento |
| **Davi** | Desenvolvimento |
| **Nicolas** | Frontend |
| **Eduardo** | Desenvolvimento |
| **Gabriel** | Desenvolvimento |

---

*Documentação detalhada de cada entrega está na respectiva pasta docs/.*
