from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Turma
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
