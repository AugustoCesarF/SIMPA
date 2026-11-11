# 🎤 Roteiro Oficial de Apresentação — SIMPA (Entrega 2)

**Sistema Inteligente de Monitoramento e Predição Acadêmica**  
**Instituição:** UniEVANGÉLICA — Centro Universitário de Anápolis  
**Curso:** Engenharia de Software / Inteligência Artificial  
**Data:** 11 de Novembro de 2026  
**Tempo Total Sugerido:** 10 a 15 minutos (Apresentação de Slides: ~8 min | Live Demo: ~4 min | Perguntas da Banca: ~3 min)  

---

## 👥 Sugestão de Divisão da Apresentação (Equipe)

- **Augusto (Líder Técnico):** Abertura, Contextualização do Problema, Arquitetura Geral e Conclusão.
- **Marcel:** Modelagem de Dados, Migração para PostgreSQL e APIs RESTful.
- **Nicolas:** Interface Visual HUD (Dark Glassmorphism), Experiência do Usuário e Live Demo.
- **Eduardo & Gabriel:** Motor Analítico de Risco Acadêmico, Inovações (IE01 a IE04) e Validações.
*(Nota: Se apenas o Augusto for apresentar, o script abaixo já está preparado de forma contínua para uma apresentação individual de alto impacto).*

---

## 📑 Índice dos Slides

1. [Slide 1: Capa & Apresentação do SIMPA](#slide-1-capa--apresentação-do-simpa)
2. [Slide 2: O Problema Real & A Proposta de Valor](#slide-2-o-problema-real--a-proposta-de-valor)
3. [Slide 3: Evolução da Entrega 1 para a Entrega 2](#slide-3-evolução-da-entrega-1-para-a-entrega-2)
4. [Slide 4: Arquitetura de Produção (MVT + REST + PostgreSQL)](#slide-4-arquitetura-de-produção-mvt--rest--postgresql)
5. [Slide 5: Modelagem de Dados & Integridade Referencial](#slide-5-modelagem-de-dados--integridade-referencial)
6. [Slide 6: Segurança, LGPD & Validação Algorítmica](#slide-6-segurança-lgpd--validação-algorítmica)
7. [Slide 7: Motor Analítico & Predição de Risco Acadêmico](#slide-7-motor-analítico--predição-de-risco-acadêmico)
8. [Slide 8: Funcionalidades de Inovação (IE01 a IE04)](#slide-8-funcionalidades-de-inovação-ie01-a-ie04)
9. [Slide 9: Demonstração Prática (Live Demo)](#slide-9-demonstração-prática-live-demo)
10. [Slide 10: Resultados Obtidos & Próximos Passos](#slide-10-resultados-obtidos--próximos-passos)
11. [Slide 11: Conclusão & Agradecimentos](#slide-11-conclusão--agradecimentos)

---

## 🎙️ Roteiro Slide a Slide (Falas e Telas)

---

### Slide 1: Capa & Apresentação do SIMPA
**Tempo estimado:** 45 segundos  
**Apresentador:** Augusto  

#### 🖥️ Conteúdo Visual do Slide
- **Título:** SIMPA — Sistema Inteligente de Monitoramento e Predição Acadêmica
- **Subtítulo:** Entrega 2: Arquitetura de Produção, Backend Django MVT e Inteligência de Risco
- **Equipe:** Augusto César F. (Líder), Marcel, Nicolas, Eduardo, Gabriel
- **Instituição:** UniEVANGÉLICA — Centro Universitário de Anápolis
- **Badges:** `Django 5.2` | `DRF` | `PostgreSQL` | `Chart.js` | `Python 3.12+`

#### 🗣️ Script de Fala Exato
> "Boa noite a todos os professores e colegas.  
> Hoje temos o prazer de apresentar a **Entrega 2** do nosso projeto: o **SIMPA** — Sistema Inteligente de Monitoramento e Predição Acadêmica.  
> 
> O SIMPA nasceu com o propósito de transformar a gestão acadêmica universitária, integrando dados em tempo real para detectar precocemente estudantes em risco de evasão e reprovação.  
> 
> Nesta segunda entrega, realizamos um salto fundamental: transformamos nossa prova de conceito preliminar em uma **plataforma completa de nível de produção**, com arquitetura Django MVT, banco de dados PostgreSQL, APIs RESTful, um motor analítico de predição de risco e uma interface visual executiva moderna. Vamos mostrar agora como cada um desses pilares foi construído."

---

### Slide 2: O Problema Real & A Proposta de Valor
**Tempo estimado:** 1 minuto  
**Apresentador:** Augusto / Marcel  

#### 🖥️ Conteúdo Visual do Slide
- **Dores do Cenário Atual:**
  - Diagnóstico tardio: a instituição só descobre a desistência ou reprovação quando o semestre já acabou.
  - Fragmentação: notas ficam em um sistema, chamadas em outro, e a comunicação com alunos é dispersa.
  - Falta de métricas preventivas: ausência de correlação entre frequência e desempenho contínuo.
- **A Solução do SIMPA:**
  - **Monitoramento Ativo:** Indicadores descritivos automáticos por turma e aluno.
  - **Predição Preventiva:** Algoritmo que calcula um score de risco de 0 a 100 com alertas e recomendações.
  - **Integração Completa:** Vida acadêmica centralizada, incluindo localização de salas e comunicação rápida.

#### 🗣️ Script de Fala Exato
> "Nas universidades brasileiras, a evasão escolar e o baixo rendimento acadêmico costumam ser diagnosticados tarde demais. Quando o professor fecha as notas da N2 ou N3, o aluno já acumulou faltas e não há mais tempo pedagógico hábil para recuperação.  
> 
> O SIMPA atua exatamente nessa ferida. Nossa proposta de valor é **antecipar o diagnóstico**. Através do cruzamento contínuo entre assiduidade, notas parciais e tendências de aprendizado, o sistema não apenas exibe números em uma tabela, mas sinaliza para a coordenação e para o professor: *'Atenção, este aluno precisa de apoio pedagógico agora'*.  
> 
> E nesta Entrega 2, garantimos que toda essa inteligência funcione sobre uma base de dados sólida, segura e pronta para escala institucional."

---

### Slide 3: Evolução da Entrega 1 para a Entrega 2
**Tempo estimado:** 1 minuto  
**Apresentador:** Marcel / Augusto  

#### 🖥️ Conteúdo Visual do Slide
- **Comparativo Direto em Tabela:**

| Critério | Entrega 1 (Protótipo) | Entrega 2 (Produção Atual) |
|---|---|---|
| **Framework** | Flask (Monolítico simples) | **Django 5.2 + Django REST Framework** |
| **Persistência** | Memória / Mock em lista Python | **PostgreSQL com integridade relacional** |
| **Arquitetura** | Scripts centralizados | **MVT Modular + Camada de Serviços desacoplada** |
| **Segurança** | Senhas estáticas | **Token Authentication, .env e proteção CSRF** |
| **Validação** | Manual básica | **Algorítmica rigorosa (CPF oficial, unicidade)** |
| **Analytics** | Regras fixas simples | **Estatística descritiva + Pearson + Score de Risco** |
| **Interface** | HTML estático | **HUD Dark Glassmorphism + Gráficos Chart.js** |

#### 🗣️ Script de Fala Exato
> "Na Entrega 1, apresentamos um protótipo inicial em Flask com dados em memória, cujo objetivo era validar a viabilidade do conceito e o web scraper do Moodle.  
> 
> Para a Entrega 2, o desafio foi a profissionalização completa da engenharia de software do projeto. Migramos para o ecossistema **Django 5.2**, adotando o padrão **MVT (Model-View-Template)** junto ao **Django REST Framework**.  
> 
> Substituímos a persistência volátil pelo **PostgreSQL**, garantindo atomicidade, índices e integridade referencial. Além disso, estruturamos uma camada de serviços dedicada para cálculos estatísticos, implementamos validações reais de documentos e renovamos completamente a interface visual com foco em ergonomia e produtividade."

---

### Slide 4: Arquitetura de Produção (MVT + REST + PostgreSQL)
**Tempo estimado:** 1 minuto e 15 segundos  
**Apresentador:** Augusto / Marcel  

#### 🖥️ Conteúdo Visual do Slide
- **Diagrama de Blocos da Arquitetura:**
  - `Browser / Cliente` ⇄ `Roteador Central (config/urls.py)`
  - `Camada Views (MVT & ViewSets)` ⇄ `Camada Services (analytics & comunidade)`
  - `Camada Models (ORM)` ⇄ `Banco de Dados PostgreSQL (localhost:5432)`
  - `Templates Engine` ⇄ `Componentes Visuais Chart.js & HUD`
- **Separação em Apps Independentes:**
  - `estudantes/` — Domínio de dados cadastrais e perfil discente
  - `turmas/` — Domínio de disciplinas, alocações e salas
  - `registros/` — Histórico de notas, frequências e dashboard geral
  - `analytics/` — Funções estatísticas puras e inteligência preditiva
  - `comunidade/` — Fórum de apoio, WhatsApp e locais de aula

#### 🗣️ Script de Fala Exato
> "Arquiteturalmente, o SIMPA foi estruturado seguindo os princípios de modularidade e separação de responsabilidades (SoC).  
> 
> O Django atua como maestro através de duas frentes complementares:  
> 1. Na frente **MVT tradicional**, as views renderizam templates HTML modernos com dados pré-processados pelo backend, garantindo carregamento rápido e sem atrito.  
> 2. Na frente **REST API**, utilizamos os ViewSets e Serializers do Django REST Framework, expondo endpoints JSON padronizados com controle de autenticação por token.  
> 
> Uma decisão crucial da nossa engenharia foi a criação da pasta `services.py`. As regras de negócio e os cálculos matemáticos complexos não poluem nem os Models nem as Views. Eles residem em serviços desacoplados e testáveis isoladamente."

---

### Slide 5: Modelagem de Dados & Integridade Referencial
**Tempo estimado:** 1 minuto  
**Apresentador:** Marcel  

#### 🖥️ Conteúdo Visual do Slide
- **Entidades de Domínio Relacional:**
  - `Estudante`: Nome, RA (único), CPF (validado), E-mail, Telefone, Curso, Status.
  - `Turma`: Código (único), Disciplina, Carga Horária, Período, Docente, Relação N:N com Estudante.
  - `LocalAula`: Campus, Bloco, Sala, Capacidade, Recursos (IE04).
  - `RegistroAcademico`: Chaves estrangeiras para Aluno e Turma, notas $N_1, N_2, N_3$, faltas totais e situação calculada.
  - `TopicoDuvida` & `PerfilUsuario`: Entidades do módulo de comunidade e interação.
- **Constraints do Banco de Dados:**
  - `unique_together` entre Estudante e Turma no Registro Acadêmico (um aluno só tem um registro por turma).
  - Normalização relacional de 3ª Forma Normal (3FN), eliminando redundâncias.

#### 🗣️ Script de Fala Exato
> "A integridade dos dados acadêmicos é essencial. No PostgreSQL, modelamos um esquema relacional robusto na terceira forma normal.  
> 
> O modelo `Estudante` controla a unicidade do RA e a validação do CPF. O modelo `Turma` estabelece uma relação Many-to-Many com os alunos e uma Foreign Key com o `LocalAula`, permitindo saber em qual bloco e sala cada aula acontece.  
> 
> Por fim, o `RegistroAcademico` amarra aluno e turma com uma constraint de unicidade: o sistema impede qualquer inconsistência de notas duplicadas e calcula automaticamente se o aluno está Aprovado, em Recuperação, Reprovado por Nota ou Reprovado por Falta segundo o regimento acadêmico."

---

### Slide 6: Segurança, LGPD & Validação Algorítmica
**Tempo estimado:** 1 minuto  
**Apresentador:** Eduardo / Gabriel  

#### 🖥️ Conteúdo Visual do Slide
- **Validação de Entrada Estrita (RNF01):**
  - Validador oficial de CPF (módulo 11 da Receita Federal com cálculo dos dois dígitos verificadores).
  - Sanitização de strings para prevenção contra *XSS* e *SQL Injection*.
- **Conformidade com a LGPD:**
  - Anonimização de dados sensíveis em relatórios públicos.
  - Armazenamento seguro de senhas com algoritmos de hash PBKDF2 / SHA-256 do Django.
- **Isolamento de Credenciais:**
  - `python-dotenv` isolando credenciais do PostgreSQL, chaves de API do WhatsApp e `SECRET_KEY` no arquivo `.env`.
  - `.env` rigidamente listado no `.gitignore`, evitando vazamento em repositórios públicos.

#### 🗣️ Script de Fala Exato
> "Em conformidade com o requisito não-funcional RNF01 e as diretrizes da LGPD, a segurança foi tratada como prioridade.  
> 
> Nos Serializers do DRF, implementamos a validação algorítmica real do CPF. O sistema rejeita CPFs com dígitos inválidos ou sequências repetidas antes mesmo de consultar o banco.  
> 
> Todas as senhas utilizam hashing PBKDF2 com salt. As credenciais de banco e chaves de serviços externos estão blindadas em arquivo `.env` fora do controle de versão. E os endpoints sensíveis possuem proteção contra CSRF e autenticação baseada em Tokens."

---

### Slide 7: Motor Analítico & Predição de Risco Acadêmico
**Tempo estimado:** 1 minuto e 30 segundos  
**Apresentador:** Augusto / Eduardo  

#### 🖥️ Conteúdo Visual do Slide
- **Módulo Analítico (`analytics/services.py`):**
  - Estatística Descritiva: Média ($\mu$), Mediana ($Md$), Desvio Padrão ($\sigma$) e Coeficiente de Variação ($CV\%$).
  - Correlação Linear de Pearson ($r$): Mede o impacto direto da assiduidade sobre a nota do estudante.
  - Tendência de Evolução: Avaliação da trajetória de notas ($N_1 \to N_2 \to N_3$).
- **Score Ponderado de Risco (0 a 100):**
  - **Fórmula:** $\text{Score} = w_1 \cdot \text{Déficit Nota} + w_2 \cdot \text{Taxa Faltas} + w_3 \cdot \text{Tendência}$
  - Faixas de Classificação:
    - 🟢 **Baixo Risco (0 - 39):** Desempenho estável e assíduo.
    - 🟡 **Médio Risco (40 - 69):** Alerta em uma avaliação ou frequência limítrofe.
    - 🔴 **Alto Risco (70 - 100):** Risco iminente de reprovação; recomendação automática de tutoria e intervenção.

#### 🗣️ Script de Fala Exato
> "O coração inteligente do SIMPA é o nosso módulo analítico. Não nos limitamos a calcular uma média simples.  
> 
> Em nosso serviço analítico, calculamos o desvio padrão e o coeficiente de variação para compreender a homogeneidade da turma. Calculamos a **Correlação de Pearson** entre faltas e notas, comprovando matematicamente o reflexo da assiduidade no aprendizado.  
> 
> E a predição heurística de risco gera um Score Ponderado de 0 a 100. Se um aluno tira nota baixa na N1 e começa a faltar, seu score salta para a faixa vermelha (Alto Risco). O sistema emite automaticamente um alerta preventivo com recomendações pedagógicas, permitindo que a coordenação atue semanas antes do fechamento do semestre."

---

### Slide 8: Funcionalidades de Inovação (IE01 a IE04)
**Tempo estimado:** 1 minuto  
**Apresentador:** Nicolas / Gabriel  

#### 🖥️ Conteúdo Visual do Slide
- **Inovações Desenvolvidas Além dos Requisitos Básicos:**
  - **IE01 — Perfil e Avatar do Usuário:** Foto/avatar dinâmico, biografia, curso e preferências.
  - **IE02 — Fórum de Comunidade e Dúvidas:** Ambiente colaborativo para perguntas entre alunos e professores com marcação de resposta resolvida.
  - **IE03 — Integração com WhatsApp:** Conexão preparada com a Meta Cloud API para envio de alertas acadêmicos e links diretos dos grupos da turma.
  - **IE04 — Central de Locais de Aula:** Mapeamento inteligente de Campus, Bloco, Sala e Horário para facilitar a localização física dos estudantes.

#### 🗣️ Script de Fala Exato
> "Além dos requisitos obrigatórios, integramos quatro módulos de inovação para enriquecer a experiência acadêmica da UniEVANGÉLICA.  
> 
> Criamos o perfil personalizado do estudante (IE01), um fórum interno de dúvidas aluno-professor com filtro de tópicos resolvidos (IE02), e a central de localização de salas de aula (IE04), que elimina a desorientação de calouros e veteranos no campus.  
> 
> E através da integração com WhatsApp (IE03), o aluno encontra com um clique o link do grupo oficial da sua turma e o sistema fica preparado para emitir avisos de risco de forma automatizada."

---

### Slide 9: Demonstração Prática (Live Demo)
**Tempo estimado:** 4 a 5 minutos  
**Apresentador:** Nicolas (Navegando) & Augusto (Explicando)  

#### 🖥️ Roteiro Prático da Demonstração ao Vivo
1. **Inicialização do Servidor:**
   - Abrir o terminal no diretório da Entrega 2:
     ```powershell
     cd C:\Users\augus\Projetos\SIMPA\Entrega2 ; python manage.py runserver
     ```
   - Mostrar a inicialização limpa: `Starting development server at http://127.0.0.1:8000/`.

2. **Passo 1: O Dashboard HUD Escuro (`/`):**
   - Abrir `http://127.0.0.1:8000/`.
   - Destacar o design moderno: Dark Theme, Glassmorphism, métricas rápidas no topo (Total de Alunos, Média Geral, Taxa de Aprovação, Alunos em Risco Crítico).
   - Mostrar a tabela de estudantes com ordenação, filtros de pesquisa e badges coloridos de situação.

3. **Passo 2: O Motor de Risco em Ação:**
   - Clicar em um aluno com Risco Alto (vermelho).
   - Mostrar os detalhes: motivo do risco (ex: frequência abaixo de 75% + nota N1 < 5.0) e a recomendação pedagógica gerada automaticamente.

4. **Passo 3: O Módulo Analítico & Gráficos (`/analytics/`):**
   - Acessar `http://127.0.0.1:8000/analytics/`.
   - Mostrar os 4 gráficos interativos em Chart.js:
     - Histograma de Distribuição de Notas.
     - Gráfico de Dispersão (Correlação Nota vs Frequência).
     - Comparativo de Médias por Turma com linha de corte (6.0).
     - Gráfico Donut de Taxa de Aprovação.

5. **Passo 4: Central de Locais de Aula e Comunidade (`/comunidade/locais/`):**
   - Mostrar os blocos e salas cadastradas e o botão direto para o grupo de WhatsApp da disciplina.

---

### Slide 10: Resultados Obtidos & Próximos Passos
**Tempo estimado:** 1 minuto  
**Apresentador:** Augusto  

#### 🖥️ Conteúdo Visual do Slide
- **Metas Alcançadas na Entrega 2:**
  - ✅ 100% dos Requisitos Funcionais RF01 a RF09 implementados e validados.
  - ✅ Requisitos Não-Funcionais RNF01 a RNF04 plenamente atendidos (Segurança, MVT Modular, Qualidade e Documentação).
  - ✅ Banco relacional PostgreSQL integrado com sucesso e migrações aplicadas.
  - ✅ Sistema testado e pronto para uso real pela comunidade acadêmica.
- **Próximos Passos (Ciclo 3 / Entrega Final):**
  - Implementação de modelos de Machine Learning supervisionados (Scikit-Learn: regressão logística e Random Forest para predição contínua).
  - Integração direta com a API oficial do AVA / Moodle da UniEVANGÉLICA via webhooks.
  - Deploy em nuvem (Railway / AWS) com banco de dados gerenciado.

#### 🗣️ Script de Fala Exato
> "Os resultados da Entrega 2 comprovam a solidez da nossa engenharia. Entregamos uma aplicação robusta, com todos os requisitos funcionais e não-funcionais cumpridos, código coberto por boas práticas e uma interface que encanta pela usabilidade.  
> 
> Para as próximas etapas, levaremos o motor de predição a um novo patamar através de algoritmos de Machine Learning com Scikit-Learn e aprofundaremos a sincronização em tempo real com o AVA Moodle da instituição."

---

### Slide 11: Conclusão & Agradecimentos
**Tempo estimado:** 30 segundos  
**Apresentador:** Augusto / Toda a Equipe  

#### 🖥️ Conteúdo Visual do Slide
- **SIMPA — Sistema Inteligente de Monitoramento e Predição Acadêmica**
- "Transformando dados em oportunidades de sucesso acadêmico."
- **Repositório GitHub:** `https://github.com/AugustoCesarF/SIMPA.git`
- **Agradecimentos:** Ao professor orientador e à UniEVANGÉLICA.
- **Abertura para Perguntas da Banca:** *Estamos à disposição para arguição.*

#### 🗣️ Script de Fala Exato
> "Em nome de toda a equipe — Augusto, Marcel, Nicolas, Eduardo e Gabriel —, agradecemos a atenção dos professores e colegas.  
> 
> O SIMPA não é apenas um trabalho acadêmico; é uma ferramenta pensada para fazer a diferença na vida dos estudantes da UniEVANGÉLICA.  
> 
> Estamos agora totalmente abertos às perguntas e observações da banca avaliadora. Muito obrigado!"

---

## 🛡️ Guia de Defesa: 10 Perguntas Difíceis da Banca & Respostas

### 1. "Por que vocês migraram de Flask para Django na Entrega 2?"
> **Resposta:** "O Flask foi excelente para a prova de conceito e validação rápida de rotas na Entrega 1. Porém, para uma aplicação acadêmica corporativa, o Django nos fornece *out-of-the-box* um ORM maduro, proteções automáticas de segurança (CSRF, Clickjacking, SQL Injection), um sistema de autenticação e permissões consolidado, e o ecossistema do Django REST Framework para criação de APIs com serializers rigorosos. Isso aumentou nossa produtividade e garantiu um padrão arquitetural MVT profissional."

### 2. "Como funciona exatamente o cálculo do score de risco acadêmico?"
> **Resposta:** "Nosso motor de risco, implementado em `analytics/services.py`, utiliza um modelo heurístico ponderado que avalia três vetores: o déficit da média do aluno em relação à nota de corte institucional (6.0), a taxa percentual de faltas em relação ao limite regimental de 25%, e o vetor de tendência entre as avaliações parciais ($N_1$ para $N_2$). O resultado é normalizado em uma escala de 0 a 100, onde scores a partir de 70 disparam alertas automáticos de intervenção."

### 3. "Como vocês garantiram a conformidade com a LGPD?"
> **Resposta:** "Implementamos o princípio de *Privacy by Design*. Dados sensíveis de estudantes têm validação rigorosa de entrada para impedir injeções; as senhas são criptografadas com hash PBKDF2; dados de contato e relatórios analíticos não expõem informações confidenciais para usuários não autenticados; e todas as chaves de conexão estão isoladas em variáveis de ambiente, nunca sendo expostas no Git."

### 4. "Como foi feita a validação de CPF nos estudantes?"
> **Resposta:** "Não usamos apenas máscaras ou validação de tamanho. Implementamos no serializer a rotina algorítmica oficial da Receita Federal, que calcula os dois dígitos verificadores através do algoritmo Módulo 11 com pesos decrescentes, além de rejeitar CPFs com todos os dígitos iguais."

### 5. "O que acontece se uma nota ou frequência for lançada como ausente ou nula?"
> **Resposta:** "Atendendo ao requisito RNF03 de qualidade de dados, nossos serviços estatísticos e serializers tratam valores nulos através de coerção segura: valores ausentes são tratados com fallbacks controlados (`valor or 0.0`), impedindo exceções como `TypeError` ou divisão por zero durante os cálculos de médias, desvios ou correlação."

### 6. "Qual a utilidade prática do Coeficiente de Pearson e do Coeficiente de Variação?"
> **Resposta:** "A média isolada muitas vezes mascara a realidade de uma turma. O Coeficiente de Variação ($CV\%$) mede a dispersão relativa: um CV alto indica uma turma muito heterogênea, com alunos brilhantes e outros muito atrasados, exigindo nivelamento. Já a Correlação de Pearson ($r$) demonstra matematicamente ao professor o quanto as faltas estão impactando negativamente as notas daquela turma específica."

### 7. "Por que manter views MVT tradicionais e também ViewSets da REST API?"
> **Resposta:** "Essa é uma arquitetura híbrida estratégica. As views MVT renderizam o Dashboard HUD principal diretamente do servidor com velocidade e sem sobrecarga de compilação de frameworks frontend. Já os ViewSets do DRF garantem interoperabilidade: o SIMPA está preparado para conectar futuramente aplicativos mobile (Flutter/React Native) ou consumir dados do AVA sem mexer na lógica de negócios."

### 8. "Como os locais de aula e grupos de WhatsApp estão modelados no banco?"
> **Resposta:** "Criamos o modelo `LocalAula` com campus, bloco, sala e capacidade. A `Turma` possui uma Foreign Key apontando para o seu local de aula e campos para horário, dia da semana e o link seguro do grupo de WhatsApp daquela disciplina. Assim, quando o aluno acessa o painel, ele visualiza onde terá aula hoje e acessa a comunicação da turma em tempo real."

### 9. "Como o sistema se comporta sob concorrência e integridade de matrículas?"
> **Resposta:** "O relacionamento entre Alunos e Turmas é gerido pelo ORM do Django com integridade referencial em nível de banco de dados PostgreSQL. Na tabela de registros acadêmicos, definimos uma restrição `unique_together` entre aluno e turma, impedindo que o mesmo aluno tenha notas duplicadas para uma disciplina no mesmo período."

### 10. "Qual foi a maior dificuldade técnica enfrentada e superada nesta Entrega 2?"
> **Resposta:** "A maior dificuldade foi refatorar todo o esquema mental de dados em memória do Flask para um modelo relacional normalizado no PostgreSQL, garantindo que os cálculos estatísticos complexos e as validações de regras de negócio fossem executados com eficiência sem degradar o tempo de resposta do dashboard. A criação da camada de serviços (`services.py`) foi a solução perfeita para esse desafio."
