from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Turma, LocalAula
from estudantes.models import Estudante


class TurmaModelAndAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="prof_turma", password="password123")
        self.client.force_authenticate(user=self.user)

        self.estudante1 = Estudante.objects.create(
            nome="Mariana Costa",
            matricula="20261001",
            email="mariana@aluno.edu.br",
            curso="Inteligência Artificial",
        )
        self.estudante2 = Estudante.objects.create(
            nome="Lucas Ribeiro",
            matricula="20261002",
            email="lucas@aluno.edu.br",
            curso="Inteligência Artificial",
        )

    def test_criar_turma_sucesso(self):
        """RF02 — Cadastro de Turma/Disciplina com persistência no banco."""
        data = {
            "nome": "Banco de Dados II",
            "codigo": "BD202",
            "curso": "Inteligência Artificial",
            "periodo": "2026/2",
            "professor": "Profª. Márcia",
            "carga_horaria": 80,
            "estudantes": [self.estudante1.id],
        }
        response = self.client.post("/api/turmas/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        turma = Turma.objects.filter(codigo="BD202").first()
        self.assertIsNotNone(turma)
        self.assertEqual(turma.nome, "Banco de Dados II")
        self.assertEqual(turma.estudantes.count(), 1)
        self.assertTrue(turma.estudantes.filter(id=self.estudante1.id).exists())

    def test_validacao_codigo_duplicado(self):
        """RF02 — Rejeitar turma com código duplicado (HTTP 400)."""
        Turma.objects.create(
            nome="Turma Alpha",
            codigo="ALP01",
            curso="IA",
            periodo="2026/2",
        )
        data = {
            "nome": "Turma Beta",
            "codigo": "ALP01",
            "curso": "IA",
            "periodo": "2026/2",
        }
        response = self.client.post("/api/turmas/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("codigo", response.data)

    def test_matricular_e_desmatricular_aluno(self):
        """RF02 — Relacionamento dinâmico de matrícula/desmatrícula entre turma e aluno."""
        turma = Turma.objects.create(
            nome="Estrutura de Dados",
            codigo="ED101",
            curso="IA",
            periodo="2026/2",
        )
        # Matricular aluno
        res_matr = self.client.post(
            f"/api/turmas/{turma.id}/matricular/",
            {"estudante_id": self.estudante2.id},
            format="json",
        )
        self.assertEqual(res_matr.status_code, status.HTTP_200_OK)
        self.assertTrue(turma.estudantes.filter(id=self.estudante2.id).exists())

        # Listar alunos da turma
        res_list = self.client.get(f"/api/turmas/{turma.id}/alunos/")
        self.assertEqual(res_list.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res_list.data), 1)

        # Desmatricular aluno
        res_desm = self.client.post(
            f"/api/turmas/{turma.id}/desmatricular/",
            {"estudante_id": self.estudante2.id},
            format="json",
        )
        self.assertEqual(res_desm.status_code, status.HTTP_200_OK)
        self.assertFalse(turma.estudantes.filter(id=self.estudante2.id).exists())

    def test_cadastro_e_consulta_local_aula(self):
        """IE04 — Cadastro de local de aula e visualização integrada à turma."""
        # 1. Cadastrar local de aula
        payload_local = {
            "campus": "UniEVANGÉLICA - Campus Sede",
            "bloco": "Bloco B",
            "sala": "Lab IA 01",
            "andar": "1º Andar",
            "cidade": "Anápolis",
            "uf": "GO",
            "capacidade": 40,
            "tipo_espaco": "Laboratório de Informática",
        }
        res_local = self.client.post("/api/turmas/locais/", payload_local, format="json")
        self.assertEqual(res_local.status_code, status.HTTP_201_CREATED)
        local_id = res_local.data["id"]

        # 2. Criar turma vinculada ao local de aula
        payload_turma = {
            "nome": "Visão Computacional",
            "codigo": "VC401",
            "curso": "Inteligência Artificial",
            "periodo": "2026/2",
            "local_aula": local_id,
            "horario": "19:00 - 22:30",
            "dia_semana": "Quarta-feira",
            "link_grupo_whatsapp": "https://chat.whatsapp.com/ExemploGrupoVC2026",
        }
        res_turma = self.client.post("/api/turmas/", payload_turma, format="json")
        self.assertEqual(res_turma.status_code, status.HTTP_201_CREATED)
        turma_id = res_turma.data["id"]

        # 3. Consultar detalhes do local de aula através do endpoint dedicado da turma
        res_consulta = self.client.get(f"/api/turmas/{turma_id}/local/")
        self.assertEqual(res_consulta.status_code, status.HTTP_200_OK)
        self.assertEqual(res_consulta.data["turma"], "Visão Computacional")
        self.assertEqual(res_consulta.data["horario"], "19:00 - 22:30")
        self.assertEqual(res_consulta.data["local"]["sala"], "Lab IA 01")
        self.assertEqual(res_consulta.data["local"]["cidade"], "Anápolis")
        self.assertEqual(res_consulta.data["link_whatsapp"], "https://chat.whatsapp.com/ExemploGrupoVC2026")
