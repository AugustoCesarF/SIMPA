# 🎤 Roteiro Oficial de Apresentação com Falas da Equipe — SIMPA (Entrega 2)

**Projeto:** SIMPA — Sistema Inteligente de Monitoramento e Predição Acadêmica  
**Instituição:** UniEVANGÉLICA — Centro Universitário de Anápolis  
**Data:** 11 de Novembro de 2026  
**Tempo Total:** 10 a 15 minutos  

---

## 👥 Escala de Apresentação da Equipe

| Integrante | Papel na Apresentação | Slides / Momentos |
|---|---|:---:|
| **Augusto** | Abertura (Boa noite), Arquitetura MVT, Motor de Risco, Narração da Demo e Encerramento | Slides 1, 4, 7, 9, 11 |
| **Marcel** | Introdução (Contexto/Problema), Evolução Flask ➔ Django e Modelagem PostgreSQL | Slides 1, 2, 3, 5, 11 |
| **Eduardo** | Segurança da Informação, Algoritmo de CPF (Receita) e Conformidade LGPD | Slide 6, 10 |
| **Nicolas** | Inovações Universitárias (IE01-IE04) e Navegação Prática da Live Demo | Slides 8, 9 |
| **Gabriel** | Regras de Negócio, Cumprimento de Requisitos (RF/RNF) e Próximos Passos | Slides 7, 10 |

---

## 🎙️ Roteiro de Fala Passo a Passo (Palavra por Palavra)

---

### 🔹 SLIDE 1: Capa & Abertura Oficial
*(Visual: Título do SIMPA, badges da stack e nomes da equipe)*

**[AUGUSTO]** *(Postura firme, olhando para a banca com energia):*
> *"Boa noite aos professores da banca avaliadora, ao nosso orientador e a todos os colegas presentes.*  
>  
> *Hoje, a nossa equipe tem a honra de apresentar a **Entrega 2** do nosso projeto integrador: o **SIMPA** — Sistema Inteligente de Monitoramento e Predição Acadêmica.*  
>  
> *Nossa equipe é formada por mim, Augusto César, pelo Marcel, pelo Nicolas, pelo Eduardo e pelo Gabriel.*  
>  
> *O SIMPA foi planejado para atacar uma das dores mais críticas do ensino superior: a evasão de alunos e a perda de rendimento que não são percebidas a tempo. Passo agora a palavra ao Marcel, que vai contextualizar o problema real que enfrentamos e a nossa proposta de valor."*

**[MARCEL]** *(Assume a fala com naturalidade):*
> *"Boa noite a todos. Complementando a fala do Augusto:*  
>  
> *Nesta Entrega 2, o SIMPA passou por uma transformação completa de engenharia de software. Superamos aquela primeira prova de conceito em Flask e estruturamos uma **plataforma corporativa de produção** sobre o Django 5.2, com banco de dados PostgreSQL, APIs REST e um motor analítico preditivo em tempo real.*  
>  
> *Vamos ver agora por que isso é tão necessário na prática universitária."*

---

### 🔹 SLIDE 2: O Problema Real & A Proposta de Valor
*(Visual: Card vermelho das Dores Tradicionais vs Card verde da Solução SIMPA)*

**[MARCEL]** *(Aponta para a tela):*
> *"No dia a dia acadêmico, o diagnóstico da reprovação costuma acontecer tarde demais. Quando o professor encerra as notas da N2 ou N3, o estudante já acumulou faltas e notas baixas que tornam a recuperação impossível naquele semestre.*  
>  
> *Além disso, os dados são fragmentados: notas ficam no portal institucional, chamadas em diários físicos e a comunicação da turma espalhada em grupos paralelos.*  
>  
> *A proposta de valor do SIMPA é a **intervenção preventiva**. Através do cruzamento de notas parciais com a taxa de frequência contínua, o sistema acende alertas pedagógicos enquanto ainda há tempo hábil para recuperação."*

---

### 🔹 SLIDE 3: Evolução da Entrega 1 para a Entrega 2
*(Visual: Tabela comparativa Flask vs Django, Memória vs PostgreSQL, etc.)*

**[MARCEL]** *(Conduz com foco técnico):*
> *"Para que a banca visualize o tamanho do avanço técnico conquistado nesta Entrega 2, preparamos este comparativo direto:*  
>  
> *• **Backend:** Saímos do Flask preliminar e migramos para o **Django 5.2 com Django REST Framework**, adotando um padrão corporativo.*  
> *• **Persistência:** Abandonamos os dados em memória e implementamos o **PostgreSQL**, com integridade relacional em 3ª Forma Normal.*  
> *• **Segurança:** Implementamos autenticação via Tokens no DRF e validação algorítmica real de documentos.*  
> *• **Interface:** Substituímos o protótipo básico pelo nosso **HUD Dark Glassmorphism**, integrando gráficos dinâmicos com Chart.js.*  
>  
> *Agora, o Augusto vai explicar como organizamos a arquitetura interna desse novo backend."*

---

### 🔹 SLIDE 4: Arquitetura de Produção (MVT + DRF + Services)
*(Visual: 3 colunas — Views MVT, Camada de Serviços desacoplada e PostgreSQL)*

**[AUGUSTO]** *(Assume com foco em arquitetura de software):*
> *"Obrigado, Marcel.*  
>  
> *Arquiteturalmente, o SIMPA foi construído sob o princípio de separação de responsabilidades (SoC).*  
>  
> *Nós dividimos a aplicação em duas frentes complementares dentro do Django:*  
> *1. As **views MVT nativas**, que processam e renderizam as telas do Dashboard direto no servidor com tempo de carregamento mínimo.*  
> *2. Os **ViewSets da REST API**, que fornecem endpoints JSON autenticados por token, garantindo que o SIMPA possa se conectar a aplicativos móveis ou ao próprio sistema da UniEVANGÉLICA.*  
>  
> *E o ponto alto da nossa arquitetura é a camada `services.py`. Não permitimos que regras de negócio ou cálculos estatísticos complexos poluam Models ou Views. Criamos módulos de serviços isolados, o que torna o código limpo, modular e fácil de testar."*

---

### 🔹 SLIDE 5: Modelagem de Dados & Integridade no PostgreSQL
*(Visual: Entidades Estudante, Turma, LocalAula, RegistroAcademico e regras de integridade)*

**[MARCEL]** *(Detalha a modelagem relacional):*
> *"Na camada de banco de dados, mapeamos entidades que refletem com fidelidade a realidade universitária:*  
> *• O `Estudante`, com controle de RA único e CPF validado.*  
> *• A `Turma`, com código único, período e relação Many-to-Many com os alunos.*  
> *• O `LocalAula`, mapeando campus, bloco físico e sala.*  
> *• E o `RegistroAcademico`, que armazena as notas N1, N2 e N3, além do total de faltas.*  
>  
> *Para blindar a consistência dos dados, criamos uma constraint `unique_together` entre estudante e turma. Isso impede que existam notas duplicadas de um mesmo aluno na mesma matéria. E o próprio modelo calcula automaticamente a situação: Aprovado, Recuperação ou Reprovado por Nota ou Falta.*  
>  
> *Passo a palavra ao Eduardo, que vai apresentar as medidas de segurança e conformidade da nossa plataforma."*

---

### 🔹 SLIDE 6: Segurança, LGPD & Validação de CPF
*(Visual: Validação Módulo 11, Criptografia PBKDF2 e isolamento no .env)*

**[EDUARDO]** *(Fala com foco em conformidade e regras de segurança):*
> *"Boa noite a todos.*  
>  
> *Atendendo ao requisito não-funcional RNF01 e à LGPD, a segurança foi aplicada desde a concepção do código.*  
>  
> *No cadastro de estudantes, não utilizamos máscaras superficiais. Implementamos no Serializer o cálculo real do **Módulo 11 da Receita Federal**, que valida os dois dígitos verificadores e barra CPFs inválidos ou repetidos antes de tocar o banco de dados.*  
>  
> *Além disso, as senhas de usuários são criptografadas com hash PBKDF2 e SHA-256 com salt. E nenhuma credencial de banco, token de WhatsApp ou chave secreta fica salva no código: todas as variáveis sensíveis são injetadas via arquivo `.env`, rigidamente bloqueado pelo `.gitignore`.*  
>  
> *Agora o Augusto vai detalhar o funcionamento do nosso motor de inteligência e risco."*

---

### 🔹 SLIDE 7: Motor Analítico & Predição de Risco Acadêmico
*(Visual: Fórmulas estatísticas, Correlação de Pearson e Score Ponderado 0 a 100)*

**[AUGUSTO]** *(Apresenta a parte analítica e matemática):*
> *"O núcleo inteligente do SIMPA está em `analytics/services.py`.*  
>  
> *Nós implementamos rotinas estatísticas descritivas completas: calculamos a média, a mediana e o **Coeficiente de Variação (CV%)**, que nos diz se a turma está homogênea ou se há um abismo entre as notas dos alunos.*  
>  
> *Também calculamos a **Correlação Linear de Pearson (r)** entre o número de faltas e o rendimento da nota, comprovando com rigor matemático o impacto da presença em sala.*  
>  
> *E o principal: nosso motor heurístico gera um **Score Ponderado de Risco de 0 a 100**, avaliando déficit de notas, taxa de faltas e tendência das avaliações parciais. Scores acima de 70 disparam alertas críticos com sugestões automáticas de intervenção pedagógica."*

---

### 🔹 SLIDE 8: Inovações Integradas à Vida Universitária (IE01 a IE04)
*(Visual: 4 cards coloridos com Perfil, Dúvidas, WhatsApp e Locais de Sala)*

**[NICOLAS]** *(Apresenta as inovações com entusiasmo):*
> *"Boa noite a todos.*  
>  
> *Para tornar o SIMPA um ecossistema completo para a UniEVANGÉLICA, desenvolvemos quatro inovações que vão além dos requisitos padrão:*  
> *• **IE01 — Perfil do Usuário:** com avatar dinâmico e biografia acadêmica personalizada.*  
> *• **IE02 — Fórum de Dúvidas:** um espaço colaborativo onde alunos publicam dúvidas por disciplina e professores podem marcar respostas resolvidas.*  
> *• **IE03 — Integração WhatsApp:** com links oficiais dos grupos de cada turma e estrutura pronta para a Meta Cloud API.*  
> *• **IE04 — Central de Locais de Aula:** um guia rápido de campus, bloco e sala física para orientar os alunos.*  
>  
> *E agora, vamos ver tudo isso funcionando ao vivo na nossa demonstração prática!"*

---

### 🔹 SLIDE 9: Demonstração Prática ao Vivo (Live Demo)
*(Ação: Nicolas pilota o navegador na tela projetada e Augusto narra os passos)*

**[NICOLAS]** *(Abre o navegador em `http://127.0.0.1:8000/` e navega suavemente)*  
**[AUGUSTO]** *(Narra em sincronia com o Nicolas):*

> *"Iniciamos nosso servidor Django na porta 8000 com banco PostgreSQL ativo.*  
>  
> *(Nicolas mostra o topo do Dashboard)*  
> *Aqui está o nosso **Dashboard HUD Principal**. Notem o tema escuro em glassmorphism e os cards de topo com as métricas consolidadas da instituição em tempo real.*  
>  
> *(Nicolas clica na linha de um aluno com badge vermelho de Alto Risco)*  
> *Ao clicar neste aluno classificado em Alto Risco, o sistema abre o diagnóstico instantâneo: ele aponta exatamente a nota baixa somada à frequência abaixo de 75%, e já recomenda o encaminhamento para a tutoria acadêmica.*  
>  
> *(Nicolas navega para `/analytics/`)*  
> *Indo para o módulo analítico, temos quatro gráficos interativos gerados com Chart.js: a dispersão de Pearson, o histograma de notas da turma e o comparativo de desempenho com a linha de corte 6.0.*  
>  
> *(Nicolas navega para `/comunidade/locais/`)*  
> *E aqui nos locais de aula, o estudante encontra o bloco, a sala e o botão que abre diretamente o grupo oficial da disciplina no WhatsApp.*  
>  
> *Passo a palavra ao Gabriel para apresentar o balanço dos requisitos cumpridos."*

---

### 🔹 SLIDE 10: Resultados Obtidos & Próximos Passos
*(Visual: Checklist de metas alcançadas e roadmap para Entrega Final)*

**[GABRIEL]** *(Fala com segurança sobre os resultados):*
> *"Boa noite a todos.*  
>  
> *Como resultado da Entrega 2, temos o orgulho de informar que atingimos **100% de conformidade** com os Requisitos Funcionais de RF01 a RF09 e com os Requisitos Não-Funcionais de RNF01 a RNF04.*  
>  
> *O backend em Django e o banco PostgreSQL estão plenamente integrados, e a interface foi elogiada pela clareza e agilidade nos testes preliminares.*  
>  
> *Para a próxima fase, daremos o próximo passo: adicionaremos **modelos de Machine Learning supervisionados com Scikit-Learn** para predição contínua e aprofundaremos a integração direta com o AVA Moodle da UniEVANGÉLICA."*

---

### 🔹 SLIDE 11: Conclusão & Agradecimentos
*(Visual: Mensagem de encerramento, link do GitHub e convite para a banca)*

**[AUGUSTO]** *(Com postura de liderança, finaliza a apresentação):*
> *"Para concluir, o SIMPA comprova que a engenharia de software e a inteligência de dados, quando bem aplicadas, são ferramentas poderosas para salvar trajetórias acadêmicas e combater o abandono universitário.*  
>  
> *Agradecemos imensamente à UniEVANGÉLICA, ao nosso professor orientador e a todos os presentes pela oportunidade de desenvolver um projeto com impacto social e acadêmico real.*  
>  
> *Eu, o Marcel e toda a nossa equipe estamos agora totalmente à disposição da banca para a arguição e perguntas. Muito obrigado!"*

---

## 🛡️ "Colinha" de Respostas Rápidas para a Banca

- **Se perguntarem a você (Augusto):** *"Por que Django e não Flask?"*  
  👉 *"O Flask serviu bem para a validação inicial. O Django nos forneceu segurança nativa contra SQL Injection e CSRF, ORM relacional maduro com PostgreSQL e serializers rigorosos no Django REST Framework para suportar escala corporativa."*

- **Se perguntarem ao Marcel:** *"Qual foi a vantagem do PostgreSQL sobre dados em memória?"*  
  👉 *"O PostgreSQL garantiu persistência durável, suporte a transações ACID, integridade referencial com chaves estrangeiras e a constraint unique_together, que impede qualquer duplicidade de notas."*

- **Se perguntarem ao Eduardo:** *"Como a LGPD foi aplicada?"*  
  👉 *"Aplicamos o conceito de Privacy by Design: validação estrita de dados de entrada, anonimização em relatórios analíticos, isolamento de credenciais no `.env` e armazenamento de senhas com algoritmo de hash PBKDF2."*

- **Se perguntarem ao Gabriel:** *"Como funciona a Correlação de Pearson na prática?"*  
  👉 *"A correlação de Pearson varia de -1 a +1. No SIMPA, ela mede matematicamente a força da relação entre o número de faltas e as notas parciais, provando ao professor como a ausência está prejudicando o aproveitamento daquela turma."*
