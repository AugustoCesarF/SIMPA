# SIMPA - Entrega 2

**Sistema Integrado de Monitoramento do Progresso Acadêmico**

## Objetivo
Evoluir o SIMPA para organizar informações acadêmicas, acompanhar estudantes e disponibilizar uma API REST.

## Estrutura
- pp/ — Sistema original, telas HTML e integração planejada com o AVA/Moodle.
- django_backend/ — Backend Django, modelos e API REST.
- docs/ — Documentação técnica e relatórios.
- ssets/ — Imagens e recursos da apresentação.

## Tecnologias
- Python 3
- Django
- Django REST Framework
- PostgreSQL
- HTML e CSS

## Funcionalidades implementadas
- Modelos de estudantes, turmas e registros acadêmicos.
- API REST com autenticação por token.
- Painel administrativo Django.
- Migrações do banco de dados.
- Painel web.

## Executar o backend
Configure o PostgreSQL e as variáveis de ambiente antes de executar o projeto.
A partir da pasta django_backend, instale as dependências e execute as migrações antes de iniciar o servidor.

## Segurança
- Não enviar o arquivo .env ao GitHub.
- Não publicar senhas ou tokens.
- A integração real com o AVA/Moodle depende de autorização e documentação da instituição.

## Observação
Esta pasta contém a cópia da Entrega 2. A pasta SIMPA/ na raiz permanece como versão de trabalho.
