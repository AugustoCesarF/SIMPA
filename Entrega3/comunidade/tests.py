from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import PerfilUsuario, TopicoDuvida, RespostaDuvida, LogNotificacaoWhatsApp
from turmas.models import Turma
from estudantes.models import Estudante


class ExtrasFuncionalidadesTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="aluno_estatistica",
            email="aluno.estat@aluno.edu.br",
            password="senha_forte_123",
            first_name="Lucas",
            last_name="Fernandes",
        )
        self.user_outro = User.objects.create_user(
            username="prof_monitor",
            email="prof.monitor@docente.edu.br",
            password="senha_forte_123",
            first_name="Prof",
            last_name="Monitor",
        )
        self.client.force_authenticate(user=self.user)

        self.turma = Turma.objects.create(
            nome="Probabilidade e Estatística",
            codigo="EST201",
            curso="Inteligência Artificial",
            periodo="2026/2",
        )

        self.estudante = Estudante.objects.create(
            nome="Lucas Fernandes",
            matricula="20269001",
            email="aluno.estat@aluno.edu.br",
            telefone="62998877665",
            curso="Inteligência Artificial",
        )

    # -----------------------------------------------------------------------
    # IE01 — Avatar / Perfil
    # -----------------------------------------------------------------------
    def test_visualizar_e_editar_perfil_avatar(self):
        """IE01 — Consulta e edição de avatar/perfil com persistência vinculada ao usuário."""
        # 1. Visualizar perfil
        res_get = self.client.get("/api/perfil/")
        self.assertEqual(res_get.status_code, status.HTTP_200_OK)
        self.assertEqual(res_get.data["username"], "aluno_estatistica")
        self.assertIn("avatar_exibicao", res_get.data)

        # 2. Editar perfil e avatar
        payload = {
            "avatar_url": "https://minha-imagem.com/avatar.png",
            "biografia": "Estudante do 2º período de IA focado em Aprendizado de Máquina.",
            "telefone": "(62) 99887-7665",
            "cidade": "Anápolis",
            "uf": "GO",
            "curso": "Inteligência Artificial",
        }
        res_put = self.client.put("/api/perfil/", payload, format="json")
        self.assertEqual(res_put.status_code, status.HTTP_200_OK)
        self.assertEqual(res_put.data["avatar_url"], "https://minha-imagem.com/avatar.png")
        self.assertEqual(res_put.data["biografia"], payload["biografia"])

        # 3. Validar persistência no banco
        perfil = PerfilUsuario.objects.get(user=self.user)
        self.assertEqual(perfil.avatar_url, "https://minha-imagem.com/avatar.png")
        self.assertEqual(perfil.cidade, "Anápolis")

    # -----------------------------------------------------------------------
    # IE02 — Comunidade: Publicação de Dúvidas e Respostas
    # -----------------------------------------------------------------------
    def test_publicar_duvida_e_responder(self):
        """IE02 — Publicação de dúvidas, respostas e identificação correta dos autores."""
        # 1. Publicar dúvida
        payload_duvida = {
            "titulo": "Dúvida sobre Desvio-Padrão Amostral vs Populacional",
            "conteudo": "Como calcular o desvio-padrão no pandas usando n-1 ou n?",
            "disciplina_nome": "Estatística Descritiva",
            "turma": self.turma.id,
        }
        res_duvida = self.client.post("/api/comunidade/duvidas/", payload_duvida, format="json")
        self.assertEqual(res_duvida.status_code, status.HTTP_201_CREATED)
        duvida_id = res_duvida.data["id"]
        self.assertEqual(res_duvida.data["autor_username"], "aluno_estatistica")
        self.assertFalse(res_duvida.data["resolvido"])

        # 2. Outro usuário responde à dúvida
        client_outro = APIClient()
        client_outro.force_authenticate(user=self.user_outro)

        payload_resposta = {
            "conteudo": "Por padrão o pandas usa ddof=1 (amostral). Se quiser populacional, use ddof=0.",
            "eh_solucao": True,
        }
        res_resp = client_outro.post(
            f"/api/comunidade/duvidas/{duvida_id}/responder/",
            payload_resposta,
            format="json",
        )
        self.assertEqual(res_resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res_resp.data["autor_username"], "prof_monitor")

        # 3. Autor marca a dúvida como resolvida
        res_resolv = self.client.post(f"/api/comunidade/duvidas/{duvida_id}/marcar-resolvido/")
        self.assertEqual(res_resolv.status_code, status.HTTP_200_OK)
        self.assertTrue(res_resolv.data["resolvido"])

        # 4. Validar consulta do tópico com respostas aninhadas
        res_detalhe = self.client.get(f"/api/comunidade/duvidas/{duvida_id}/")
        self.assertEqual(res_detalhe.status_code, status.HTTP_200_OK)
        self.assertEqual(res_detalhe.data["total_respostas"], 1)
        self.assertEqual(res_detalhe.data["respostas"][0]["autor_username"], "prof_monitor")

    # -----------------------------------------------------------------------
    # IE03 — Integração WhatsApp (Conformidade com API Oficial Meta)
    # -----------------------------------------------------------------------
    def test_whatsapp_status_e_notificacao_risco(self):
        """IE03 — Auditoria e envio de alerta com documentação de dependência externa e grupos."""
        # 1. Consulta de status e conformidade oficial de grupos
        res_status = self.client.get("/api/comunidade/whatsapp/")
        self.assertEqual(res_status.status_code, status.HTTP_200_OK)
        self.assertIn("politica_meta_grupos", res_status.data)
        self.assertIn("integracao_oficial", res_status.data)

        # 2. Disparar notificação de risco para aluno
        payload_notif = {
            "aluno_id": self.estudante.id,
            "motivo_risco": "Média abaixo de 5.0 em Estatística",
            "recomendacao": "Agendar reforço na tutoria",
        }
        res_envio = self.client.post("/api/comunidade/whatsapp/", payload_notif, format="json")
        self.assertEqual(res_envio.status_code, status.HTTP_200_OK)
        self.assertTrue(res_envio.data["sucesso"])
        self.assertIn("link_acionamento_direto", res_envio.data)
        self.assertEqual(res_envio.data["status"], "PENDENTE_AUTORIZACAO_API")
        self.assertTrue(len(res_envio.data["dependencias_externas"]) > 0)

        # 3. Validar registro de log no banco
        log = LogNotificacaoWhatsApp.objects.filter(estudante=self.estudante).first()
        self.assertIsNotNone(log)
        self.assertEqual(log.status_envio, "PENDENTE_AUTORIZACAO_API")
        self.assertIn("Média abaixo de 5.0", log.mensagem)
