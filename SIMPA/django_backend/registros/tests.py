from decimal import Decimal
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from rest_framework import status

from estudantes.models import Estudante
from turmas.models import Turma
from .models import RegistroAcademico


class RegistrosEAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="coordenador",
            email="coord@simpa.edu.br",
            password="senha_segura_123",
            first_name="Carlos",
            last_name="Silva",
        )
        self.client.force_authenticate(user=self.user)

        self.estudante = Estudante.objects.create(
            nome="Beatriz Souza",
            matricula="20262001",
            email="beatriz@aluno.edu.br",
            curso="Inteligência Artificial",
        )
        self.turma = Turma.objects.create(
            nome="Algoritmos Avançados",
            codigo="AA301",
            curso="Inteligência Artificial",
            periodo="2026/2",
        )

    def test_criar_registro_sucesso(self):
        """RF03/RF07 — Cadastro de registro acadêmico e persistência."""
        data = {
            "estudante": self.estudante.id,
            "turma": self.turma.id,
            "periodo": "2026/2",
            "nota": "8.50",
            "frequencia": "92.00",
            "observacoes": "Excelente desempenho em sala.",
        }
        response = self.client.post("/api/registros/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["situacao"], "Aprovado")
        self.assertFalse(response.data["em_risco"])

        # Persistência
        reg = RegistroAcademico.objects.filter(estudante=self.estudante, turma=self.turma).first()
        self.assertIsNotNone(reg)
        self.assertEqual(reg.nota, Decimal("8.50"))

    def test_validacao_nota_invalida(self):
        """RF03 — Rejeitar nota fora do intervalo [0.00, 10.00] (HTTP 400)."""
        data = {
            "estudante": self.estudante.id,
            "turma": self.turma.id,
            "periodo": "2026/2",
            "nota": "11.50",
            "frequencia": "80.00",
        }
        response = self.client.post("/api/registros/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("nota", response.data)

    def test_validacao_frequencia_invalida(self):
        """RF03 — Rejeitar frequência fora do intervalo [0.00, 100.00] (HTTP 400)."""
        data = {
            "estudante": self.estudante.id,
            "turma": self.turma.id,
            "periodo": "2026/2",
            "nota": "7.00",
            "frequencia": "105.00",
        }
        response = self.client.post("/api/registros/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("frequencia", response.data)

    def test_indicadores_academicos(self):
        """RF04/RF05/RF07 — Rota /api/indicadores/ calcula métricas e estatísticas descritivas."""
        RegistroAcademico.objects.create(
            estudante=self.estudante,
            turma=self.turma,
            periodo="2026/2",
            nota=Decimal("7.50"),
            frequencia=Decimal("90.00"),
        )
        response = self.client.get("/api/indicadores/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("estatisticas_notas", response.data)
        self.assertIn("media", response.data["estatisticas_notas"])
        self.assertIn("mediana", response.data["estatisticas_notas"])
        self.assertIn("situacao", response.data)

    def test_relatorios_consolidados(self):
        """RF06/RF07 — Rota /api/relatorios/ consolida turmas e ranking de alunos."""
        RegistroAcademico.objects.create(
            estudante=self.estudante,
            turma=self.turma,
            periodo="2026/2",
            nota=Decimal("9.00"),
            frequencia=Decimal("95.00"),
        )
        response = self.client.get("/api/relatorios/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("turmas", response.data)
        self.assertIn("ranking_alunos", response.data)

    def test_risco_aluno_especifico(self):
        """RF09 — Endpoint de predição e análise de risco acadêmico por aluno."""
        RegistroAcademico.objects.create(
            estudante=self.estudante,
            turma=self.turma,
            periodo="2026/2",
            nota=Decimal("3.50"),
            frequencia=Decimal("60.00"),
        )
        response = self.client.get(f"/api/risco/{self.estudante.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["nivel"], "ALTO")
        self.assertTrue(len(response.data["motivos"]) > 0)
        self.assertTrue(len(response.data["recomendacoes"]) > 0)


class AuthTokenTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="docente1",
            email="docente1@simpa.edu.br",
            password="minha_senha_secreta",
            first_name="Docente",
            last_name="Exemplo",
        )

    def test_login_por_username_sucesso(self):
        """RF08 — Obtenção de Token simples via POST /api/auth/token/ com username."""
        data = {"username": "docente1", "password": "minha_senha_secreta"}
        response = self.client.post("/api/auth/token/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)
        self.assertEqual(response.data["username"], "docente1")

    def test_login_por_email_sucesso(self):
        """RF08 — Obtenção de Token simples via POST /api/auth/token/ com e-mail."""
        data = {"email": "docente1@simpa.edu.br", "password": "minha_senha_secreta"}
        response = self.client.post("/api/auth/token/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)

    def test_login_credenciais_invalidas(self):
        """RF08 — Rejeitar credenciais erradas com HTTP 401."""
        data = {"username": "docente1", "password": "senha_errada"}
        response = self.client.post("/api/auth/token/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("error", response.data)

    def test_autenticacao_obrigatoria_com_token(self):
        """RF08 — Requisições a endpoints protegidos exigem token de autenticação."""
        unauthenticated_client = APIClient()

        # Sem token → 401 Unauthorized
        response_sem_token = unauthenticated_client.get("/api/estudantes/")
        self.assertEqual(response_sem_token.status_code, status.HTTP_401_UNAUTHORIZED)

        # Com token válido no cabeçalho Authorization: Token <key>
        token = Token.objects.create(user=self.user)
        authenticated_client = APIClient()
        authenticated_client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

        response_com_token = authenticated_client.get("/api/estudantes/")
        self.assertEqual(response_com_token.status_code, status.HTTP_200_OK)

        # Testar /api/auth/me/
        response_me = authenticated_client.get("/api/auth/me/")
        self.assertEqual(response_me.status_code, status.HTTP_200_OK)
        self.assertEqual(response_me.data["username"], "docente1")

        # Testar /api/auth/logout/ (revogação)
        response_logout = authenticated_client.post("/api/auth/logout/")
        self.assertEqual(response_logout.status_code, status.HTTP_200_OK)
        self.assertFalse(Token.objects.filter(user=self.user).exists())
