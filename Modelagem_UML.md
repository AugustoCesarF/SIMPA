# Modelagem UML - SIMPA

Este documento apresenta os diagramas conceituais estruturados durante a Semana 3 do Ciclo 1.
Eles podem ser visualizados em qualquer renderizador Mermaid (como o próprio visualizador nativo do GitHub).

## 1. Diagrama de Casos de Uso

```mermaid
usecaseDiagram
    actor "Administrador (Coordenação)" as Admin
    actor "Sistema AVA (Moodle)" as Moodle
    
    package "SIMPA - Sistema Inteligente de Monitoramento" {
        usecase "Fazer Login" as UC1
        usecase "Sincronizar Dados do AVA" as UC2
        usecase "Visualizar Painel de Indicadores" as UC3
        usecase "Gerenciar Alunos (CRUD)" as UC4
        usecase "Gerenciar Matrículas" as UC5
        usecase "Consultar Análise de Risco" as UC6
    }
    
    Admin --> UC1
    Admin --> UC3
    Admin --> UC4
    Admin --> UC5
    Admin --> UC6
    
    UC1 ..> UC2 : <<extend>> (Login via Moodle)
    UC2 <-- Moodle : Fornece notas e cursos
    UC6 ..> UC3 : <<include>>
```

## 2. Diagrama de Classes (Domínio)

Este diagrama reflete as classes implementadas no arquivo `app/models.py` (Semana 4).

```mermaid
classDiagram
    class Usuario {
        +int id
        +String nome
        +String email
        +String senha_hash
        +String perfil
        +autenticar(senha) bool
    }

    class Aluno {
        +String matricula_ra
        +List~RegistroAcademico~ registros
        +get_media_geral() float
    }

    class Professor {
        +String departamento
        +List~Turma~ turmas_lecionadas
    }

    class Disciplina {
        +int id
        +String codigo
        +String nome
        +int carga_horaria
    }

    class Turma {
        +int id
        +String codigo_turma
        +String periodo
        +adicionar_aluno(Aluno)
    }

    class RegistroAcademico {
        +float nota1
        +float nota2
        +float nota3
        +int faltas
        +String situacao
        +calcular_media_final() float
        +atualizar_situacao()
    }

    class IndicadorRisco {
        +float score_percentual
        +List~String~ motivos
        +List~String~ recomendacoes
        +Date data_calculo
        +get_nivel_risco() String
    }

    class APIService {
        +String base_url
        +fetch_dados_aluno(matricula) dict
    }

    Usuario <|-- Aluno : Herança
    Usuario <|-- Professor : Herança
    Turma "1" *-- "1" Disciplina : contém
    Turma "1" o-- "many" Professor : lecionado por
    RegistroAcademico "many" *-- "1" Aluno : pertence a
    RegistroAcademico "many" *-- "1" Turma : referente a
    IndicadorRisco "1" o-- "1" Aluno : avalia
```
