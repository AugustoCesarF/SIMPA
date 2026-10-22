from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Estudante
from turmas.models import Turma


class EstudanteModelAndAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="prof_teste", password="password123")
        self.client.force_authenticate(user=self.user)

        self.turma = Turma.objects.create(
            nome="Inteligência Artificial - Turma A",
            codigo="IA201",
            curso="Inteligência Artificial",
            periodo="2026/2",
        )

    def test_criar_estudante_sucesso(self):
        """RF01 — Cadastro de aluno com dados válidos e persistência no banco."""
        data = {
            "nome": "João Pedro Santos",
            "matricula": "20260101",
            "cpf": "11144477735",  # CPF com dígitos válidos
            "email": "joao.santos@aluno.edu.br",
            "curso": "Inteligência Artificial",
            "turma_id": self.turma.id,
        }
        response = self.client.post("/api/estudantes/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verificar persistência no banco
        estudante = Estudante.objects.filter(matricula="20260101").first()
        self.assertIsNotNone(estudante)
        self.assertEqual(estudante.nome, "João Pedro Santos")
        self.assertEqual(estudante.email, "joao.santos@aluno.edu.br")

        # Verificar relacionamento com a turma
        self.assertTrue(self.turma.estudantes.filter(id=estudante.id).exists())

    def test_validacao_matricula_duplicada(self):
        """RF01 — Rejeitar cadastro com matrícula duplicada (HTTP 400)."""
        Estudante.objects.create(
            nome="Aluno Um",
            matricula="20269999",
            email="um@teste.com",
            curso="IA",
        )
        data = {
            "nome": "Aluno Dois",
            "matricula": "20269999",
            "email": "dois@teste.com",
            "curso": "IA",
        }
        response = self.client.post("/api/estudantes/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("matricula", response.data)

    def test_validacao_cpf_invalido(self):
        """RF01 — Rejeitar cadastro com CPF inválido (HTTP 400)."""
        data = {
            "nome": "Carlos Teste",
            "matricula": "20260102",
            "cpf": "12345678900",  # CPF matematicamente inválido
            "email": "carlos@teste.com",
            "curso": "IA",
        }
        response = self.client.post("/api/estudantes/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("cpf", response.data)

    def test_validacao_nome_obrigatorio(self):
        """RF01 — Rejeitar estudante sem nome ou com nome vazio (HTTP 400)."""
        data = {
            "nome": "   ",
            "matricula": "20260103",
            "email": "teste@teste.com",
            "curso": "IA",
        }
        response = self.client.post("/api/estudantes/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_alias_alunos_funciona(self):
        """RF07 — Rota /api/alunos/ deve operar identicamente a /api/estudantes/."""
        response = self.client.get("/api/alunos/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
