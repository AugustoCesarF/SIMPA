"""
models.py
Arquivo de estruturação orientada a objetos (Semana 4).
Representa as entidades centrais do sistema SIMPA para a camada de persistência.
No futuro (Ciclo 2), estas classes serão convertidas em Models do Django/MySQL.
"""
from datetime import datetime
from typing import List, Optional

class Usuario:
    def __init__(self, id: int, nome: str, email: str, senha_hash: str, perfil: str):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha_hash = senha_hash
        self.perfil = perfil  # 'admin', 'professor', 'aluno'
        self.ativo = True

    def autenticar(self, senha_tentativa: str) -> bool:
        # Lógica de validação de hash (bcrypt) a ser implementada
        pass

class Aluno(Usuario):
    def __init__(self, id: int, nome: str, email: str, senha_hash: str, matricula_ra: str):
        super().__init__(id, nome, email, senha_hash, perfil='aluno')
        self.matricula_ra = matricula_ra
        self.registros: List['RegistroAcademico'] = []

    def get_media_geral(self) -> float:
        if not self.registros:
            return 0.0
        return sum(r.calcular_media_final() for r in self.registros) / len(self.registros)

class Professor(Usuario):
    def __init__(self, id: int, nome: str, email: str, senha_hash: str, departamento: str):
        super().__init__(id, nome, email, senha_hash, perfil='professor')
        self.departamento = departamento
        self.turmas_lecionadas: List['Turma'] = []

class Disciplina:
    def __init__(self, id: int, codigo: str, nome: str, carga_horaria: int):
        self.id = id
        self.codigo = codigo
        self.nome = nome
        self.carga_horaria = carga_horaria

class Turma:
    def __init__(self, id: int, codigo_turma: str, periodo: str, disciplina: Disciplina, professor: Professor):
        self.id = id
        self.codigo_turma = codigo_turma
        self.periodo = periodo
        self.disciplina = disciplina
        self.professor = professor
        self.alunos_matriculados: List[Aluno] = []

    def adicionar_aluno(self, aluno: Aluno):
        self.alunos_matriculados.append(aluno)

class RegistroAcademico:
    def __init__(self, id: int, aluno: Aluno, turma: Turma):
        self.id = id
        self.aluno = aluno
        self.turma = turma
        self.nota1: float = 0.0
        self.nota2: float = 0.0
        self.nota3: float = 0.0
        self.faltas: int = 0
        self.situacao: str = 'Em Curso'

    def calcular_media_final(self) -> float:
        return round((self.nota1 + self.nota2 + self.nota3) / 3, 2)

    def atualizar_situacao(self):
        media = self.calcular_media_final()
        if self.faltas > (self.turma.disciplina.carga_horaria * 0.25): # Exemplo: 25% de faltas reprova
            self.situacao = 'Reprovado por Falta'
        elif media >= 6.0:
            self.situacao = 'Aprovado'
        elif media >= 4.0:
            self.situacao = 'Recuperação'
        else:
            self.situacao = 'Reprovado'

class APIService:
    """Classe responsável por simular a conexão com o AVA"""
    def __init__(self, base_url: str):
        self.base_url = base_url

    def fetch_dados_aluno(self, matricula: str) -> dict:
        # Integração com moodle_scraper entraria aqui
        pass

class IndicadorRisco:
    def __init__(self, aluno: Aluno, score_percentual: float, motivos: List[str], recomendacoes: List[str]):
        self.aluno = aluno
        self.score_percentual = score_percentual
        self.motivos = motivos
        self.recomendacoes = recomendacoes
        self.data_calculo = datetime.now()

    def get_nivel_risco(self) -> str:
        if self.score_percentual <= 25: return "BAIXO"
        elif self.score_percentual <= 55: return "MÉDIO"
        else: return "ALTO"
